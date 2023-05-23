from django.urls import path, include, re_path
from .views import (
    ThingList,
    ThingDetail,

    FaceList,
    FaceDetail,

    LicensePlateList,
    LicensePlateDetail,

    FacePredictionList,
    FacePredictionDetail,

    LicensePlatePredictionList,
    LicensePlatePredictionDetail
)

urlpatterns = [
    path('api/thing', ThingList.as_view()),
    path('api/thing/<int:thing_id>/', ThingDetail.as_view()),

    path('api/face', FaceList.as_view()),
    path('api/face/<int:face_id>/', FaceDetail.as_view()),

    path('api/license-plate', LicensePlateList.as_view()),
    path('api/license-plate/<int:license_plate_id>/', LicensePlateDetail.as_view()),

    path('api/face-prediction', FacePredictionList.as_view()),
    path('api/face-prediction/<int:face_prediction_id>/', FacePredictionDetail.as_view()),

    path('api/license-plate-prediction', LicensePlatePredictionList.as_view()),
    path('api/license-plate-prediction/<int:license_plate_prediction_id>/', LicensePlatePredictionDetail.as_view())
]
