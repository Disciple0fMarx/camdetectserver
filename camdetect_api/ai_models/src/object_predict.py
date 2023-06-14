import io
import torch
import torchvision
from PIL import Image

MODEL_PATH = 'camdetect_api/ai_models/weights/yolov5s.pt'


def load_model(model_path):
    # Load YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, device='cpu')
    return model

def predict_image(model, image_path):
    # Load image
    image = Image.open(image_path)
    
    # Make prediction
    results = model(image)
    
    # Extract prediction information
    pred_classes = results.pandas().xyxy[0]['name'].tolist()
    pred_confidence = results.pandas().xyxy[0]['confidence'].tolist()    
    
    return pred_classes, pred_confidence


def predict_frame(model, frame):
    # Load image
    image = Image.fromarray(frame)
    
    # Make prediction
    results = model(image)
    
    # Extract prediction information
    pred_classes = results.pandas().xyxy[0]['name'].tolist()
    pred_confidence = results.pandas().xyxy[0]['confidence'].tolist()    
    
    return pred_classes, pred_confidence


def perform_object_prediction(image_path: str) -> str:
    # Load YOLOv5 model
    model = load_model(MODEL_PATH)
    pred_classes, pred_confidence = predict_image(model, image_path)
    # Format the results
    results = []
    for pred_class, confidence in zip(pred_classes, pred_confidence):
        results.append(f'{pred_class} ({confidence * 100:.2f}%)')
    return ', '.join(results)


def convert_mjpeg_to_jpeg(mjpeg_frame):
    # Create a BytesIO object to hold the MJPEG frame
    mjpeg_bytes = io.BytesIO(mjpeg_frame)

    # Open the MJPEG frame as an image using PIL
    image = Image.open(mjpeg_bytes)

    # Convert the image to JPEG format
    jpeg_bytes = io.BytesIO()
    image.save(jpeg_bytes, format='JPEG')
    jpeg_bytes.seek(0)

    # Return the converted JPEG image as bytes
    return jpeg_bytes.getvalue()


def perform_object_prediction_video(frame: str) -> str:
    # Load YOLOv5 model
    model = load_model(MODEL_PATH)
    pred_classes, pred_confidence = predict_frame(model, frame)
    # Format the results
    results = []
    for pred_class, confidence in zip(pred_classes, pred_confidence):
        results.append(f'{pred_class} ({confidence * 100:.2f}%)')
    return ', '.join(results)


def main():
    # Load YOLOv5 model
    model = load_model('weights/yolov5s.pt')

    # Predict on an image
    image_path = '/home/dhya/Downloads/airbud.jpg'
    pred_classes, pred_confidence = predict_image(model, image_path)

    # Format the results
    results = []
    for pred_class, confidence in zip(pred_classes, pred_confidence):
        results.append(f'{pred_class} ({confidence * 100:.2f}%)')
        
    # Print predictions
    print('Here are the objects predicted in the provided image:')
    print(', '.join(results))


if __name__ == '__main__':
    main()
