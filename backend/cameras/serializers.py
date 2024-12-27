from rest_framework import serializers
from .models import Camera, Recording, CameraAccess

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ['id', 'name', 'device_id', 'is_active', 'created_at', 
                 'last_active', 'resolution', 'night_mode', 'motion_detection']
        read_only_fields = ['owner', 'created_at', 'last_active']

class RecordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recording
        fields = ['id', 'camera', 'start_time', 'end_time', 'file_path', 
                 'file_size', 'motion_triggered', 'created_at']
        read_only_fields = ['created_at']

class CameraAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraAccess
        fields = ['id', 'camera', 'user', 'can_view', 'can_control', 'created_at']
        read_only_fields = ['created_at']
