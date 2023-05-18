from rest_framework import serializers
from .models import Thing, Face, LicensePlate


class ThingSerializer(serializers.ModelSerializer):  # YOLOv5
    class Meta:
        model = Thing
        fields = ['title', 'timestamp', 'image', 'user']


class FaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Face
        fields = ['title', 'timestamp', 'image', 'user']


class LicensePlateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicensePlate
        fields = ['title', 'timestamp', 'image', 'user']
