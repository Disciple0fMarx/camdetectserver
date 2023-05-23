# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import (
    Thing,
    Face,
    LicensePlate,
    FacePrediction,
    LicensePlatePrediction
)
from .serializers import (
    ThingSerializer,
    FaceSerializer,
    LicensePlateSerializer,
    FacePredictionSerializer,
    LicensePlatePredictionSerializer
)


# Create your views here.


# List views
class ThingList(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        '''List all the Thing items.'''
        things = Thing.objects.all()
        serializer = ThingSerializer(things, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the Thing with the given Thing data.'''
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.data.get('image')
        }
        serializer = ThingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FaceList(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        '''List all the Face items.'''
        faces = Face.objects.all()
        serializer = ThingSerializer(faces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the Face with the given Face data.'''
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.data.get('image')
        }
        serializer = FaceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LicensePlateList(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        '''List all the LicensePlate items.'''
        license_plates = LicensePlate.objects.all()
        serializer = LicensePlateSerializer(license_plates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the LicensePlate with the given LicensePlate data.'''
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.data.get('image')
        }
        serializer = LicensePlateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacePredictionList(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        '''List all the FacePrediction items for the given requested face.'''
        face_predictions = FacePrediction.objects.all()
        serializer = FacePredictionSerializer(face_predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the FacePrediction with the given FacePrediction data.'''
        data = {
            'inference_image': request.data.get('inference_image'),
            'result': request.data.get('result'),
            'face': request.data.get('face')
        }
        serializer = FacePredictionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LicensePlatePredictionList(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        '''List all the LicensePlatePrediction items for the given requested license plate.'''
        license_plate_predictions = LicensePlatePrediction.objects.all()
        serializer = LicensePlatePredictionSerializer(license_plate_predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the LicensePlatePrediction with the given LicensePlatePrediction data.'''
        data = {
            'inference_image': request.data.get('inference_image'),
            'result': request.data.get('result'),
            'license_plate': request.data.get('license_plate')
        }
        serializer = LicensePlatePredictionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Detail views
class ThingDetail(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, thing_id):
        '''Helper method to get the object with the given thing_id.'''
        try:
            return Thing.objects.get(id=thing_id)
        except Thing.DoesNotExist:
            return None

    def get(self, request, thing_id, *args, **kwargs):
        '''Retrieves the Thing with given thing_id.'''
        thing_instance = self.get_object(thing_id)
        if not thing_instance:
            return Response(
                {'res': 'Object with thing_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ThingSerializer(thing_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, thing_id, *args, **kwargs):
        '''Updates the Thing item with the given thing_id if it exists.'''
        thing_instance = self.get_object(thing_id)
        if not thing_instance:
            return Response(
                {'res': 'Object with thing_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.data.get('image')
        }
        serializer = ThingSerializer(instance=thing_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, thing_id, *args, **kwargs):
        '''Deletes the Thing item with the given thing_id if it exists.'''
        thing_instance = self.get_object(thing_id)
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


class FaceDetail(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, face_id):
        '''Helper method to get the object with the given face_id.'''
        try:
            return Face.objects.get(id=face_id)
        except Face.DoesNotExist:
            return None

    def get(self, request, face_id, *args, **kwargs):
        '''Retrieves the Face with given face_id.'''
        face_instance = self.get_object(face_id)
        if not face_instance:
            return Response(
                {'res': 'Object with face_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = FaceSerializer(face_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, face_id, *args, **kwargs):
        '''Updates the Face item with the given face_id if it exists.'''
        face_instance = self.get_object(face_id)
        if not face_instance:
            return Response(
                {'res': 'Object with face_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.data.get('image')
        }
        serializer = ThingSerializer(instance=face_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, face_id, *args, **kwargs):
        '''Deletes the Face item with the given face_id if it exists.'''
        face_instance = self.get_object(face_id)
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


class LicensePlateDetail(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, license_plate_id):
        '''Helper method to get the object with the given license_plate_id.'''
        try:
            return LicensePlate.objects.get(id=license_plate_id)
        except LicensePlate.DoesNotExist:
            return None

    def get(self, request, license_plate_id, *args, **kwargs):
        '''Retrieves the LicensePlate with the given license_plate_id.'''
        license_plate_instance = self.get_object(license_plate_id)
        if not license_plate_instance:
            return Response(
                {'res': 'Object with license_plate_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = LicensePlateSerializer(license_plate_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, license_plate_id, *args, **kwargs):
        '''Updates the LicensePlate item with the given license_plate_id if it exists.'''
        license_plate_instance = self.get_object(license_plate_id)
        if not license_plate_instance:
            return Response(
                {'res': 'Object with license_plate_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.data.get('image')
        }
        serializer = LicensePlateSerializer(instance=license_plate_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, license_plate_id, *args, **kwargs):
        '''Deletes the LicensePlate item with the given license_plate_id if it exists.'''
        license_plate_instance = self.get_object(license_plate_id)
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


class FacePredictionDetail(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, face_prediction_id):
        '''Helper method to get the object with the given face_prediction_id.'''
        try:
            return FacePrediction.objects.get(id=face_prediction_id)
        except FacePrediction.DoesNotExist:
            return None
    
    def get(self, request, face_prediction_id, *args, **kwargs):
        '''Retrieves the FacePrediction with the given face_prediction_id.'''
        face_prediction_instance = self.get_object(face_prediction_id)
        if not face_prediction_instance:
            return Response(
                {'res': 'Object with face_prediction_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = FacePredictionSerializer(face_prediction_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, face_prediction_id, *args, **kwargs):
        '''Updates the FacePrediction item with the given face_prediction_id if it exists.'''
        face_prediction_instance = self.get_object(face_prediction_id)
        if not face_prediction_instance:
            return Response(
                {'res': 'Object with face_prediction_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'inference_image': request.data.get('inference_image'),
            'result': request.data.get('result'),
            'face': request.data.get('face')
        }
        serializer = FacePredictionSerializer(instance=face_prediction_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, face_prediction_id, *args, **kwargs):
        '''Deletes the FacePrediction item with the given face_prediction_id if it exists.'''
        face_prediction_instance = self.get_object(face_prediction_id)
        if not face_prediction_instance:
            return Response(
                {'res': 'Object with face_prediction_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        face_prediction_instance.delete()
        return Response(
            {'res': 'Object deleted!'},
            status=status.HTTP_200_OK
        )


class LicensePlatePredictionDetail(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, license_plate_prediction_id):
        '''Helper method to get the object with the given license_plate_prediction_id.'''
        try:
            return LicensePlatePrediction.objects.get(id=license_plate_prediction_id)
        except LicensePlatePrediction.DoesNotExist:
            return None
    
    def get(self, request, license_plate_prediction_id, *args, **kwargs):
        '''Retrieves the LicensePlatePrediction with the given license_plate_prediction_id.'''
        license_plate_prediction_instance = self.get_object(license_plate_prediction_id)
        if not license_plate_prediction_instance:
            return Response(
                {'res': 'Object with license_plate_prediction_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = LicensePlatePredictionSerializer(license_plate_prediction_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, license_plate_prediction_id, *args, **kwargs):
        '''Updates the LicensePlatePrediction item with the given license_plate_prediction_id if it exists.'''
        license_plate_prediction_instance = self.get_object(license_plate_prediction_id)
        if not license_plate_prediction_instance:
            return Response(
                {'res': 'Object with license_plate_prediction_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'inference_image': request.data.get('inference_image'),
            'result': request.data.get('result'),
            'license_plate': request.data.get('license_plate')
        }
        serializer = LicensePlatePredictionSerializer(instance=license_plate_prediction_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, license_plate_prediction_id, *args, **kwargs):
        '''Deletes the LicensePlatePrediction item with the given license_plate_prediction_id if it exists.'''
        license_plate_prediction_instance = self.get_object(license_plate_prediction_id)
        if not license_plate_prediction_instance:
            return Response(
                {'res': 'Object with license_plate_prediction_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        license_plate_prediction_instance.delete()
        return Response(
            {'res': 'Object deleted!'},
            status=status.HTTP_200_OK
        )