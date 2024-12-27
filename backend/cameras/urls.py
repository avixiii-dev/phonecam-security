from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cameras', views.CameraViewSet, basename='camera')
router.register(r'recordings', views.RecordingViewSet, basename='recording')
router.register(r'camera-access', views.CameraAccessViewSet, basename='camera-access')

urlpatterns = [
    path('', include(router.urls)),
]
