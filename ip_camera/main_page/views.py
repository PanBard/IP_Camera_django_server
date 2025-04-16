from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import StreamingHttpResponse
from my_script.my_ip_camera_code import *

def video_feed(request):
    return StreamingHttpResponse( gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame' )

def one_frame(request):
    return HttpResponse(one_frame_feed(), content_type='image/jpeg') 

def home(request):
    return render(request,"home.html")

def camera(request):
    return render(request,"camera.html")

def img(request):
    return render(request,"img.html")


def all_images_list(request):
    items = IPCameraImage.objects.all()
    return render(request,"all_images_list.html", {'img_list': items})


def settings_view(request):
    items = CameraSettings.objects.first() 
    if items:
        print(items)
        return render(request,"settings.html", {'settings': items})
    else:
        print(items)
        CameraSettings.objects.create(movement_detection=True)       # If no settings object exists, create one
        return render(request,"settings.html", {'settings': items})



from django.core.files.base import ContentFile
from datetime import datetime
from .models import CameraSettings, IPCameraImage

def save_frame_to_db(request):
    print('start save_frame_to_db')
    if request.method == 'POST':
        print('inside post')
        # if latest_frame contain image from ip camera
        if stream_cache.latest_frame:
            print('inside stream_cache.latest_frame')
            image_data = stream_cache.latest_frame 
            filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            image_file = ContentFile(image_data)

            capture = IPCameraImage()
            image_title = 'Test'
            capture.title = image_title
            capture.image.save(filename, image_file)
            capture.save()
            print('end ')
    return redirect('camera')



def toggle_movement_detection(request):
    settings = CameraSettings.objects.first() # Fetch the current camera settings object
    settings.movement_detection = not settings.movement_detection        # Toggle the movement detection state to False or True
    settings.save()
    return redirect('settings_view')  # Redirect to the same page or another page after updating

def toggle_movement_detection_db_save(request):
    settings = CameraSettings.objects.first() # Fetch the current camera settings object
    settings.movement_detection_db_save = not settings.movement_detection_db_save        # Toggle the movement detection state to False or True
    settings.save()
    return redirect('settings_view')  # Redirect to the same page or another page after updating

def toggle_face_detection(request):
    settings = CameraSettings.objects.first() # Fetch the current camera settings object
    settings.face_detection = not settings.face_detection        # Toggle the movement detection state to False or True
    settings.save()
    return redirect('settings_view')  # Redirect to the same page or another page after updating

def toggle_face_detection_db_save(request):
    settings = CameraSettings.objects.first() # Fetch the current camera settings object
    settings.face_detection_db_save = not settings.face_detection_db_save        # Toggle the movement detection state to False or True
    settings.save()
    return redirect('settings_view')  # Redirect to the same page or another page after updating


def change_frame_process_interval(request):
    if request.method == 'POST':
        settings = CameraSettings.objects.first() # Fetch the current camera settings object
        new_interval = request.POST.get('frame_process_interval')
        if new_interval:
            try:
                settings.frame_process_interval = float(new_interval)  # Convert to float (if you're using decimal values)
                settings.save()
                print(f'frame_process_interval {new_interval}')
            except ValueError:
                pass  # You can add error handling here if needed
    return redirect('settings_view')  # Redirect to the same page or another page after updating