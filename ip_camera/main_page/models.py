from django.db import models

# class ToDoItem(models.Model):
#     title = models.CharField(max_length=200)
#     comleted = models.BooleanField(default=False)



class IPCameraImage(models.Model):
    title = models.CharField(max_length=200, default='Default Title')
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='ip_camera_images/')

    def __str__(self):
        return f"Image at {self.timestamp}"



class CameraSettings(models.Model):
    movement_detection = models.BooleanField(default=False)
    movement_detection_db_save = models.BooleanField(default=False)
    face_detection = models.BooleanField(default=False)
    face_detection_db_save = models.BooleanField(default=False)
    frame_process_interval = models.FloatField(default=0.5)

    def __str__(self):
        return f"Movement Detection: {self.movement_detection}"