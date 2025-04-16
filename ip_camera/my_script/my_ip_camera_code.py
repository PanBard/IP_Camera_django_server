from datetime import datetime
import cv2
import numpy as np
import requests
import time
from main_page.models import CameraSettings, IPCameraImage
from django.core.files.base import ContentFile
from . import stream_cache  # <-- import the cache module


def gen_frames():
    fgbg = cv2.createBackgroundSubtractorMOG2()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    url = 'http://192.168.0.101'
    stream = requests.get(url, stream=True)
    bytes_data = b''
    settings = CameraSettings.objects.first()

    last_process_time = time.time()
    
    motion_detected = False
    face_detected = False

    try:
        for chunk in stream.iter_content(chunk_size=1024):
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8')  # JPEG start
            b = bytes_data.find(b'\xff\xd9')  # JPEG end

            if a != -1 and b != -1:                
                jpg = bytes_data[a:b+2]
                bytes_data = bytes_data[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

               
                if time.time() - last_process_time < settings.frame_process_interval:  # Only process and yield frame every 0.5 seconds
                    continue
                last_process_time = time.time()

                if settings.face_detection:
                    # Convert the current frame to grayscale and blur it to reduce noise
                    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
                    face_detected = False  # Flag to track motion detection status
                    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)) # Detect faces in the ROI
                    # Draw rectangles around faces
                    for (fx, fy, fw, fh) in faces:
                        cv2.rectangle(frame, (fx, fy), (fx + fw, fy + fh), (255, 0, 0), 2)
                        face_detected = True
                    


                if settings.movement_detection:
                    fgmask = fgbg.apply(frame)
                    _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)# Optional: You can apply a bit of thresholding to refine the foreground mask
                    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)# Find contours of the moving areas
                    motion_detected = False  # Flag to track motion detection status
                    # Draw rectangles around moving areas
                    for contour in contours:
                        if cv2.contourArea(contour) > 10000:  # Ignore small movements
                            (x, y, w, h) = cv2.boundingRect(contour)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            motion_detected = True
                            
                    if frame is None:
                        continue
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                stream_cache.latest_frame = frame # Save the latest frame in cache
                if motion_detected and settings.movement_detection_db_save:
                    image_data = stream_cache.latest_frame 
                    filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    image_file = ContentFile(image_data)
                    capture = IPCameraImage()
                    image_title = 'Motion_detected'
                    capture.title = image_title
                    capture.image.save(filename, image_file)
                    capture.save()
                    print(f'Motion detected! - File {filename} saved!')

                if face_detected  and settings.face_detection_db_save:
                    image_data = stream_cache.latest_frame 
                    filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    image_file = ContentFile(image_data)
                    capture = IPCameraImage()
                    image_title = 'Face_detected'
                    capture.title = image_title
                    capture.image.save(filename, image_file)
                    capture.save()
                    print(f'Face detected! - File {filename} saved!')
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                # time.sleep(0.5)
                
    except GeneratorExit:
        # This is raised when the client disconnects (like closing the browser tab)
        print("Client disconnected from video stream.")
    except Exception as e:
        print(f"Stream error: {e}")
    finally:
        stream.close()
        print("Closed stream from IP camera.")



def one_frame_feed():
    fgbg = cv2.createBackgroundSubtractorMOG2()
    url = 'http://192.168.0.101'
    stream = requests.get(url, stream=True)
    bytes_data = b''

    try:
        for chunk in stream.iter_content(chunk_size=1024):
            bytes_data += chunk
            a = bytes_data.find(b'\xff\xd8')  # JPEG start
            b = bytes_data.find(b'\xff\xd9')  # JPEG end

            if a != -1 and b != -1:
                jpg = bytes_data[a:b+2]
                bytes_data = bytes_data[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                fgmask = fgbg.apply(frame)

                # Optional: You can apply a bit of thresholding to refine the foreground mask
                _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

                # Find contours of the moving areas
                contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Draw rectangles around moving areas
                for contour in contours:
                    if cv2.contourArea(contour) > 10000:  # Ignore small movements
                        (x, y, w, h) = cv2.boundingRect(contour)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if frame is None:
                    continue
                _, buffer = cv2.imencode('.jpg', frame)
                
                frame = buffer.tobytes()
                stream_cache.latest_frame = frame # Save the latest frame in cache
                
                return frame
                
    except GeneratorExit:
        print("Client disconnected from video stream.")
    except Exception as e:
        print(f"Stream error: {e}")
    finally:
        stream.close()
        print("Closed stream from IP camera.")