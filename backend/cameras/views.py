from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from .models import Camera, Recording, CameraAccess
from .serializers import CameraSerializer, RecordingSerializer, CameraAccessSerializer

class CameraViewSet(viewsets.ModelViewSet):
    serializer_class = CameraSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return cameras owned by user or shared with user
        return Camera.objects.filter(
            models.Q(owner=self.request.user) |
            models.Q(shared_with__user=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_motion_detection(self, request, pk=None):
        camera = self.get_object()
        camera.motion_detection = not camera.motion_detection
        camera.save()
        return Response({'status': 'motion detection updated'})

    @action(detail=True, methods=['post'])
    def toggle_night_mode(self, request, pk=None):
        camera = self.get_object()
        camera.night_mode = not camera.night_mode
        camera.save()
        return Response({'status': 'night mode updated'})

class RecordingViewSet(viewsets.ModelViewSet):
    serializer_class = RecordingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recording.objects.filter(
            models.Q(camera__owner=self.request.user) |
            models.Q(camera__shared_with__user=self.request.user)
        ).distinct()

class CameraAccessViewSet(viewsets.ModelViewSet):
    serializer_class = CameraAccessSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CameraAccess.objects.filter(camera__owner=self.request.user)

    def perform_create(self, serializer):
        # Ensure user can only share their own cameras
        camera = serializer.validated_data['camera']
        if camera.owner != self.request.user:
            raise permissions.PermissionDenied("You can only share cameras you own.")
        serializer.save()
