import face_recognition
import os, sys
import cv2
import numpy as np
import math
from PIL import Image


# Helper
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self, faces_dir: str):
        self.encode_faces(faces_dir)

    def encode_faces(self, faces_dir: str):
        for image in os.listdir(faces_dir):
            face_image = face_recognition.load_image_file(f"{faces_dir}/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
    
    def recognize_from_image(self, image: str) -> str:
        # Convert image to numpy array
        new_image = Image.open(image)
        image_array = np.asarray(new_image)
        # Resize image to 1/4 size for faster face recognition processing
        small_image = cv2.resize(image_array, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_image = small_image[:, :, ::-1]
        # Find all the faces and face encodings in the image
        self.face_locations = face_recognition.face_locations(rgb_small_image)
        self.face_encodings = face_recognition.face_encodings(rgb_small_image, self.face_locations)
        self.face_names = []
        for face_encoding in self.face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            confidence = '???'

            # Calculate the shortest distance to face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                confidence = face_confidence(face_distances[best_match_index])

            self.face_names.append(f'{name} ({confidence})')
            return ', '.join(self.face_names)


def main():
    fr = FaceRecognition('/home/dhya/Repos/webcam_face_recognition/faces')
    print(fr.recognize_from_image('/home/dhya/Downloads/dhya_test.jpg'))


if __name__ == '__main__':
    main()
