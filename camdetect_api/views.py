# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Thing, Face, LicensePlate
from .serializers import ThingSerializer, FaceSerializer, LicensePlateSerializer


# Create your views here.
class ThingListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        '''List all the Thing items for the given requested user.'''
        things = Thing.objects.filter(user=request.user.id)
        serializer = ThingSerializer(things, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the Thing with the given Thing data.'''
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.data.get('image'),
            'user': request.user.id
        }
        serializer = ThingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FaceListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        '''List all the Face items for the given requested user.'''
        faces = Face.objects.filter(user=request.user.id)
        serializer = ThingSerializer(faces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the Face with the given Face data.'''
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.data.get('image'),
            'user': request.user.id
        }
        serializer = FaceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LicensePlateListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        '''List all the LicensePlate items for the given requested user.'''
        license_plates = LicensePlate.objects.filter(user=request.user.id)
        serializer = LicensePlateSerializer(license_plates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the LicensePlate with the given LicensePlate data.'''
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.data.get('image'),
            'user': request.user.id
        }
        serializer = LicensePlateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
