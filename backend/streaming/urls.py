from django.urls import path
from . import views

urlpatterns = [
    path('stream/signal/<int:camera_id>/', 
         views.WebRTCSignalingView.as_view(), 
         name='webrtc-signal'),
    path('stream/health/<int:camera_id>/', 
         views.StreamHealthCheckView.as_view(), 
         name='stream-health'),
]
