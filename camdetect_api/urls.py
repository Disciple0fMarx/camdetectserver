from django.urls import path, include, re_path
from .views import (
    FaceList,
    FaceDetail,

    LicensePlateList,
    LicensePlateDetail,

    ObjectPredictionList,
    ObjectPredictionDetail,

    FacePredictionList,
    FacePredictionDetail,

    LicensePlatePredictionList,
    LicensePlatePredictionDetail,

    connect_object_camera,
    disconnect_object_camera,
    video_stream_objects,

    connect_face_camera,
    disconnect_face_camera,
    video_stream_faces,

    connect_plate_camera,
    disconnect_plate_camera,
    video_stream_plates,
)


urlpatterns = [
    path('api/face', FaceList.as_view()),
    path('api/face/<int:face_id>/', FaceDetail.as_view()),

    path('api/license-plate', LicensePlateList.as_view()),
    path('api/license-plate/<int:license_plate_id>/', LicensePlateDetail.as_view()),

    path('api/object-prediction', ObjectPredictionList.as_view()),
    path('api/object-prediction/<int:object_prediction_id>/', ObjectPredictionDetail.as_view()),

    path('api/face-prediction', FacePredictionList.as_view()),
    path('api/face-prediction/<int:face_prediction_id>/', FacePredictionDetail.as_view()),

    path('api/license-plate-prediction', LicensePlatePredictionList.as_view()),
    path('api/license-plate-prediction/<int:license_plate_prediction_id>/', LicensePlatePredictionDetail.as_view()),

    path('camera/object/connect', connect_object_camera, name='connect_object_camera'),
    path('camera/object/disconnect', disconnect_object_camera, name='disconnect_object_camera'),
    path('camera/object/video-stream', video_stream_objects, name='video_stream_objects'),

    path('camera/face/connect', connect_face_camera, name='connect_face_camera'),
    path('camera/face/disconnect', disconnect_face_camera, name='disconnect_face_camera'),
    path('camera/face/video-stream', video_stream_faces, name='video_stream_faces'),

    path('camera/license-plate/connect', connect_plate_camera, name='connect_plate_camera'),
    path('camera/license-plate/disconnect', disconnect_plate_camera, name='disconnect_plate_camera'),
    path('camera/license-plate/video-stream', video_stream_plates, name='video_stream_plates'),
]
