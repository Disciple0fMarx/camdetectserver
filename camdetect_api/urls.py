from django.urls import path, include, re_path
from .views import (
    ThingListApiView,
    ThingDetailApiView,

    FaceListApiView,
    FaceDetailApiView,

    LicensePlateListApiView,
    LicensePlateDetailApiView
)

urlpatterns = [
    path('api/thing', ThingListApiView.as_view()),
    path('api/thing/<int:thing_id>/', ThingDetailApiView.as_view()),

    path('api/face', FaceListApiView.as_view()),
    path('api/face/<int:face_id>/', FaceDetailApiView.as_view()),

    path('api/license-plate', LicensePlateListApiView.as_view()),
    path('api/license-plate/<int:license_plate_id>/', LicensePlateDetailApiView.as_view()),
]

