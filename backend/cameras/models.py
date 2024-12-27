from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Camera(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cameras')
    device_id = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    resolution = models.CharField(max_length=20, default='720p')
    night_mode = models.BooleanField(default=False)
    motion_detection = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.device_id})"

class Recording(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='recordings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    file_path = models.CharField(max_length=255)
    file_size = models.BigIntegerField(default=0)
    motion_triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recording {self.camera.name} - {self.start_time}"

class CameraAccess(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='shared_with')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='camera_access')
    can_view = models.BooleanField(default=True)
    can_control = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('camera', 'user')
