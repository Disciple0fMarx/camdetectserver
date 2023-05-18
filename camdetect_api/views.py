# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Thing, Face, LicensePlate
from .serializers import ThingSerializer, FaceSerializer, LicensePlateSerializer


# Create your views here.


# List views
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


# Detail views
class ThingDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, thing_id, user_id):
        '''Helper method to get the object with the given thing_id and user_id.'''
        try:
            return Thing.objects.get(id=thing_id, user = user_id)
        except Thing.DoesNotExist:
            return None

    def get(self, request, thing_id, *args, **kwargs):
        '''Retrieves the Thing with given thing_id.'''
        thing_instance = self.get_object(thing_id, request.user.id)
        if not thing_instance:
            return Response(
                {'res': 'Object with thing_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ThingSerializer(thing_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, thing_id, *args, **kwargs):
        '''Updates the Thing item with the given thing_id if it exists.'''
        thing_instance = self.get_object(thing_id, request.user.id)
        if not thing_instance:
            return Response(
                {'res': 'Object with thing_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.data.get('image'),
            'user': request.user.id
        }
        serializer = ThingSerializer(instance = thing_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, thing_id, *args, **kwargs):
        '''Deletes the Thing item with the given thing_id if it exists.'''
        thing_instance = self.get_object(thing_id, request.user.id)
        if not thing_instance:
            return Response(
                {'res': 'Object with thing_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        thing_instance.delete()
        return Response(
            {'res': 'Object deleted!'},
            status=status.HTTP_200_OK
        )


class FaceDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, face_id, user_id):
        '''Helper method to get the object with the given face_id and user_id.'''
        try:
            return Face.objects.get(id=face_id, user = user_id)
        except Face.DoesNotExist:
            return None

    def get(self, request, face_id, *args, **kwargs):
        '''Retrieves the Face with given face_id.'''
        face_instance = self.get_object(face_id, request.user.id)
        if not face_instance:
            return Response(
                {'res': 'Object with face_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = FaceSerializer(face_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, face_id, *args, **kwargs):
        '''Updates the Face item with the given face_id if it exists.'''
        face_instance = self.get_object(face_id, request.user.id)
        if not face_instance:
            return Response(
                {'res': 'Object with face_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.data.get('image'),
            'user': request.user.id
        }
        serializer = ThingSerializer(instance = face_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, face_id, *args, **kwargs):
        '''Deletes the Face item with the given face_id if it exists.'''
        face_instance = self.get_object(face_id, request.user.id)
        if not face_instance:
            return Response(
                {'res': 'Object with face_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        face_instance.delete()
        return Response(
            {'res': 'Object deleted!'},
            status=status.HTTP_200_OK
        )


class LicensePlateDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, license_plate_id, user_id):
        '''Helper method to get the object with the given license_plate_id and user_id.'''
        try:
            return LicensePlate.objects.get(id=license_plate_id, user = user_id)
        except LicensePlate.DoesNotExist:
            return None

    def get(self, request, license_plate_id, *args, **kwargs):
        '''Retrieves the Thing with given license_plate_id.'''
        license_plate_instance = self.get_object(license_plate_id, request.user.id)
        if not license_plate_instance:
            return Response(
                {'res': 'Object with license_plate_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = LicensePlateSerializer(license_plate_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, license_plate_id, *args, **kwargs):
        '''Updates the LIcensePlate item with the given license_plate_id if it exists.'''
        license_plate_instance = self.get_object(license_plate_id, request.user.id)
        if not license_plate_instance:
            return Response(
                {'res': 'Object with license_plate_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.data.get('image'),
            'user': request.user.id
        }
        serializer = LicensePlateSerializer(instance = license_plate_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, license_plate_id, *args, **kwargs):
        '''Deletes the LicensePlate item with the given license_plate_id if it exists.'''
        license_plate_instance = self.get_object(license_plate_id, request.user.id)
        if not license_plate_instance:
            return Response(
                {'res': 'Object with license_plate_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        license_plate_instance.delete()
        return Response(
            {'res': 'Object deleted!'},
            status=status.HTTP_200_OK
        )
