# from django.shortcuts import render
from django.http import QueryDict
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import (
    Face,
    LicensePlate,
    ObjectPrediction,
    FacePrediction,
    LicensePlatePrediction
)
from .serializers import (
    FaceSerializer,
    LicensePlateSerializer,
    ObjectPredictionSerializer,
    FacePredictionSerializer,
    LicensePlatePredictionSerializer
)
from camdetect_api.ai_models.src.face_predict import FaceRecognition
# from camdetect_api.ai_models.src.license_plate_predict import PlateReader


# Create your views here.


# List views

class FaceList(APIView):
    # # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]
    
    def get(self, request, *args, **kwargs):
        '''List all the Face items.'''
        faces = Face.objects.all()
        serializer = FaceSerializer(faces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the Face with the given Face data.'''
        data = {
            'title': request.data.get('title'),
            'timestamp': request.data.get('timestamp'),
            'image': request.FILES['image']
        }
        serializer = FaceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LicensePlateList(APIView):
    # # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]
    
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
            'image': request.FILES['image']
        }
        serializer = LicensePlateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObjectPredictionList(APIView):
    # # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]
    
    def get(self, request, *args, **kwargs):
        '''List all the ObjectPrediction items for the given requested object prediction.'''
        object_predictions = ObjectPrediction.objects.all()
        serializer = ObjectPredictionSerializer(object_predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the ObjectPrediction with the given ObjectPrediction data.'''
        data = {
            'inference_image': request.FILES['inference_image'],
            'timestamp': request.data.get('timestamp'),
            'result': request.data.get('result')
        }
        serializer = ObjectPredictionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FacePredictionList(APIView):
    # # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]
    
    def get(self, request, *args, **kwargs):
        '''List all the FacePrediction items for the given requested face.'''
        face_predictions = FacePrediction.objects.all()
        serializer = FacePredictionSerializer(face_predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the FacePrediction with the given FacePrediction data.'''
        inference_image = request.FILES['inference_image']
        # Perform face recognition on the inference image and get the result
        fr = FaceRecognition()
        result = fr.recognize_from_image(inference_image)
        # Find the matching face
        if result == 'Unknown':
            face = 0
        else:
            matching_face = get_object_or_404(Face, image='uploads/faces/'+result)
            face = matching_face.id
        data = {
            'inference_image': inference_image,
            'timestamp': request.data.get('timestamp'),
            'result': result,
            'face': face
        }
        serializer = FacePredictionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LicensePlatePredictionList(APIView):
    # # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]
    
    def get(self, request, *args, **kwargs):
        '''List all the LicensePlatePrediction items for the given requested license plate.'''
        license_plate_predictions = LicensePlatePrediction.objects.all()
        serializer = LicensePlatePredictionSerializer(license_plate_predictions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the LicensePlatePrediction with the given LicensePlatePrediction data.'''
        data = {
            'inference_image': request.FILES['inference_image'],
            'timestamp': request.data.get('timestamp'),
            'result': request.data.get('result'),
            'license_plate': request.data.get('license_plate')
        }
        serializer = LicensePlatePredictionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Detail views

class FaceDetail(APIView):
    # # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]

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
            'image': request.FILES['image']
        }
        serializer = FaceSerializer(instance=face_instance, data=data, partial=True)
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
    # # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]

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
            'image': request.FILES['image']
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


class ObjectPredictionDetail(APIView):
    # # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]

    def get_object(self, object_prediction_id):
        '''Helper method to get the object with the given object_prediction_id.'''
        try:
            return ObjectPrediction.objects.get(id=object_prediction_id)
        except ObjectPrediction.DoesNotExist:
            return None
    
    def get(self, request, object_prediction_id, *args, **kwargs):
        '''Retrieves the Prediction with the given object_prediction_id.'''
        object_prediction_instance = self.get_object(object_prediction_id)
        if not object_prediction_instance:
            return Response(
                {'res': 'Object with object_prediction_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ObjectPredictionSerializer(object_prediction_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, object_prediction_id, *args, **kwargs):
        '''Updates the ObjectPrediction item with the given object_prediction_id if it exists.'''
        object_prediction_instance = self.get_object(object_prediction_id)
        if not object_prediction_instance:
            return Response(
                {'res': 'Object with object_prediction_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'inference_image': request.FILES['inference_image'],
            'timestamp': request.data.get('timestamp'),
            'result': request.data.get('result')
        }
        serializer = ObjectPredictionSerializer(instance=object_prediction_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, object_prediction_id, *args, **kwargs):
        '''Deletes the ObjectPrediction item with the given object_prediction_id if it exists.'''
        object_prediction_instance = self.get_object(object_prediction_id)
        if not object_prediction_instance:
            return Response(
                {'res': 'Object with object_prediction_id does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        object_prediction_instance.delete()
        return Response(
            {'res': 'Object deleted!'},
            status=status.HTTP_200_OK
        )


class FacePredictionDetail(APIView):
    # # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]

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
            'inference_image': request.FILES['inference_image'],
            'timestamp': request.data.get('timestamp'),
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
    # # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]

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
            'inference_image': request.FILES['inference_image'],
            'timestamp': request.data.get('timestamp'),
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


# AI Operations

# @csrf_exempt
# def predict_face(request):
#     if request.method == 'POST':
#         inference_image = request.FILES.get('inference_image')

#         # Perform face recognition on the inference image and get the result
#         fr = FaceRecognition()
#         result = fr.recognize_from_image(inference_image)
#         # Find the matching face
#         matching_face = get_object_or_404(Face, image='uploads/faces/'+result)
#         face = matching_face.id

#         # Create a new FacePrediction instance with the result and save it to the database
#         face_prediction = FacePrediction(inference_image=inference_image, result=result, face=face)
#         face_prediction.save()