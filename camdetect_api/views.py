# from django.shortcuts import render
import cv2
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators import gzip
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_bytes
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from camdetectserver import settings
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
from camdetect_api.ai_models.src.object_predict import perform_object_prediction
from camdetect_api.ai_models.src.face_predict import FaceRecognition
from camdetect_api.ai_models.src.license_plate_predict import PlateReader


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
    # parser_classes = [MultiPartParser]
    
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
            'plate_text': request.data.get('plate_text')
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
        inference_image = request.FILES['inference_image']
        data = {
            'inference_image': inference_image,
            'timestamp': request.data.get('timestamp'),
            'result': ''
        }
        serializer = ObjectPredictionSerializer(data=data)
        if serializer.is_valid():   
            serializer.validated_data['result'] = perform_object_prediction(inference_image)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
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
        data = {
            'inference_image': inference_image,
            'timestamp': request.data.get('timestamp'),
            'result': '',
        }
        serializer = FacePredictionSerializer(data=data)
        if serializer.is_valid():
            fr = FaceRecognition()
            result = fr.recognize_from_image(inference_image)
            print(f'result: {result}')
            if result in ['Unknown', '']:
                serializer.validated_data['result'] = 'Unknown'
                random_face = Face.objects.first()
                serializer.validated_data['face'] = random_face
            else:
                matching_face = get_object_or_404(Face, image=f'faces/{result}')
                serializer.validated_data['face'] = matching_face
                serializer.validated_data['result'] = matching_face.title
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
        encoded_data = []
        for prediction in serializer.data:
            encoded_result = smart_bytes(prediction['result'], encoding='utf-8')
            prediction['result'] = encoded_result
            encoded_data.append(prediction)
        return Response(encoded_data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        '''Create the LicensePlatePrediction with the given LicensePlatePrediction data.'''
        inference_image = request.FILES['inference_image']
        data = {
            'inference_image': inference_image,
            'timestamp': request.data.get('timestamp'),
            'result': '',
        }
        serializer = LicensePlatePredictionSerializer(data=data)
        if serializer.is_valid():
            pr = PlateReader(inference_image)
            result = pr.read()
            matching_plate = pr.find_closest_match(result)
            license_plate = 0 if matching_plate == None else matching_plate
            if license_plate == 0:
                serializer.validated_data['result'] = result
                random_plate = LicensePlate.objects.first()
                serializer.validated_data['license_plate'] = random_plate
            else: 
                new_result = matching_plate.plate_text
                serializer.validated_data['result'] = new_result
            serializer.validated_data['license_plate'] = license_plate
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
        # image = os.path.relpath(face_prediction_instance.inference_image.path, settings.MEDIA_ROOT)
        # if os.path.exists(image):
        #     os.remove(image)
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


# Cameras
camera_url = None
# Object Prediction

@csrf_exempt
def connect_object_camera(request) -> Response:
    global camera_url
    '''Returns the object camera URL.'''
    try:
        camera_url = request.data.get('camera_url')
        print(f'Object camera URL: {camera_url}')
        return Response(
            {'res': 'Acquired object camera URL successfully'},
            status=status.HTTP_200_OK,
        )
    except:
        return Response(
            {'res': 'Invalid URL'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    

def stream_video_objects():
    # Replace 'your_ip_webcam_url' with the actual IP webcam URL
    IP_WEBCAM_URL = 'your_ip_webcam_url'
    cap = cv2.VideoCapture(IP_WEBCAM_URL)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Perform object detection on the frame
        processed_frame = perform_object_prediction(frame)
        # Convert the processed frame to JPEG format for streaming
        ret, jpeg = cv2.imencode('.jpg', processed_frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')


@gzip.gzip_page
def video_stream_objects(request):
    response = StreamingHttpResponse(stream_video_objects(), content_type='multipart/x-mixed-replace; boundary=frame')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def save_detected_object(request):
    if request.method == 'POST':
        # Extract and save the detected object information
        inference_image = request.POST.get('inference_image')
        timestamp = request.POST.get('timestamp')
        result = request.POST.get('result')
        # Save the information to your Django model
        prediction = ObjectPrediction(
            inference_image=inference_image,
            timestamp=timestamp,
            result=result
        )
        prediction.save()
        return JsonResponse({'message': 'Object prediction saved successfully.'}, status=201)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def get_detected_objects(request):
    if request.method == 'GET':
        # Retrieve the detected objects
        detected_objects = ObjectPrediction.objects.all()

        # Convert the detected objects to a list of dictionaries
        objects_list = []
        for obj in detected_objects:
            obj_data = {
                'inference_image': obj.inference_image,
                'timestamp': obj.timestamp,
                'result': obj.result,
            }
            objects_list.append(obj_data)

        # Return the detected objects as JSON response
        return JsonResponse(objects_list, safe=False)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
