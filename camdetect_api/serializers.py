from rest_framework import serializers
from .models import (
    Face,
    LicensePlate,

    ObjectPrediction,
    FacePrediction,
    LicensePlatePrediction
)


class FaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Face
        fields = ['id', 'title', 'timestamp', 'image']


class LicensePlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicensePlate
        fields = ['id', 'title', 'timestamp', 'plate_text']


class ObjectPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectPrediction
        fields = ['id', 'inference_image', 'timestamp', 'result']


class FacePredictionSerializer(serializers.ModelSerializer):
    face = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = FacePrediction
        fields = ['id', 'inference_image', 'timestamp', 'result', 'face']


class LicensePlatePredictionSerializer(serializers.ModelSerializer):
    license_plate = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = LicensePlatePrediction
        fields = ['id', 'inference_image', 'timestamp', 'result', 'license_plate']
