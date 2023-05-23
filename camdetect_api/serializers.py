from rest_framework import serializers
from .models import (
    Thing,
    Face,
    LicensePlate,

    FacePrediction,
    LicensePlatePrediction
)


class ThingSerializer(serializers.ModelSerializer):  # YOLOv5
    class Meta:
        model = Thing
        fields = ['title', 'timestamp', 'image']


class FaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Face
        fields = ['title', 'timestamp', 'image']


class LicensePlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicensePlate
        fields = ['title', 'timestamp', 'image']


class FacePredictionSerializer(serializers.ModelSerializer):
    face = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = FacePrediction
        fields = ['inference_image', 'result', 'face']


class LicensePlatePredictionSerializer(serializers.ModelSerializer):
    license_plate = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LicensePlatePrediction
        fields = ['inference_image', 'result', 'license_plate']
