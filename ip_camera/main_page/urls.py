from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("camera/", views.camera, name="camera"),
    path("img/", views.img, name="img"),
    path("video_feed/", views.video_feed, name="video_feed"),
    path("one_frame/", views.one_frame, name="one_frame"),
    path("save_image/", views.save_frame_to_db, name="save_image"),
    path("all_images_list/", views.all_images_list, name="all_images_list"),
    path('toggle_movement_detection/', views.toggle_movement_detection, name='toggle_movement_detection'),
    path('toggle_movement_detection_db_save/', views.toggle_movement_detection_db_save, name='toggle_movement_detection_db_save'),
    path('toggle_face_detection/', views.toggle_face_detection, name='toggle_face_detection'),
    path('toggle_face_detection_db_save/', views.toggle_face_detection_db_save, name='toggle_face_detection_db_save'),
    path('change_frame_process_interval/', views.change_frame_process_interval, name='change_frame_process_interval'),
    path("settings_view/", views.settings_view, name="settings_view")
    ]