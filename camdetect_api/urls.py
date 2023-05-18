from django.urls import path, include, re_path
from .views import (
    ThingListApiView,
    FaceListApiView,
    LicensePlateListApiView
)

urlpatterns = [
    path('api/thing', ThingListApiView.as_view()),
    path('api/face', FaceListApiView.as_view()),
    path('api/license-plate', LicensePlateListApiView.as_view())
]

