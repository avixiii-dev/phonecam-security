from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cameras.models import Camera
import json

class WebRTCSignalingView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, camera_id):
        try:
            camera = Camera.objects.get(id=camera_id)
            # Check if user has access to the camera
            if not (camera.owner == request.user or 
                   camera.shared_with.filter(user=request.user).exists()):
                return Response(
                    {"error": "No access to this camera"}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Handle WebRTC signaling data
            signal_data = request.data.get('signal')
            if not signal_data:
                return Response(
                    {"error": "No signal data provided"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Here you would implement the actual WebRTC signaling logic
            # This is a placeholder for the actual implementation
            return Response({"status": "signal received"})

        except Camera.DoesNotExist:
            return Response(
                {"error": "Camera not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class StreamHealthCheckView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, camera_id):
        try:
            camera = Camera.objects.get(id=camera_id)
            if camera.owner != request.user:
                return Response(
                    {"error": "Not the camera owner"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            # Update camera's last_active timestamp
            camera.save()  # This will update the auto_now field
            return Response({"status": "health check received"})

        except Camera.DoesNotExist:
            return Response(
                {"error": "Camera not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
