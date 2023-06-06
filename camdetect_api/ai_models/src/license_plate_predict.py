import requests
# import json
import cv2
# from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
from PIL import Image
from jellyfish import jaro_winkler
from camdetect_api.models import LicensePlate
from django.shortcuts import get_object_or_404


IMAGE_PATH: str = '/home/dhya/Downloads/dataset/image_tn.jpeg'
DEPLOYMENT_URL: str = 'https://inf-cb2925ad-7007-4946-a561-4a8c73f907d6-no4xvrhsfq-uc.a.run.app/detect'


class PlateReader:
    def __init__(self, image_path=IMAGE_PATH):
        self.image_path = image_path
    
    def detect_from_theos_ai(self, deployment_url=DEPLOYMENT_URL, conf_thres=.25, iou_thres=.45, ocr_model='medium', ocr_classes='lp', ocr_languages='ara') -> list[dict]:
        '''
        Returns the license plate prediction data from the model on Theos AI* .
        
        * For more information on Theos AI, visit https://blog.theos.ai/.
        '''
        response = requests.post(
            deployment_url,
            data={
                'conf_thres': conf_thres,
                'iou_thres': iou_thres,
                'ocr_model': ocr_model,
                'ocr_classes': ocr_classes,
                'ocr_languages': ocr_languages
            },
            files={
                'image': open(self.image_path, 'rb')
            }
        )
        if response.status_code in [200, 500]:
            data = response.json()
            print(data)
            if 'error' in data:
                print('[!]', data['message'])
            else:
                return data
        elif response.status_code == 403:
            print('[!] you reached your monthly requests limit. Upgrade your plan to unlock unlimited requests.')
        return [{}]
    
    def read(self):
        new_image = Image.open(self.image_path)
        image_array = np.asarray(new_image)
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction
        edged = cv2.Canny(bfilter, 30, 200)  # Edge detection
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], 0, 255, -1)
        new_image = cv2.bitwise_and(image_array, image_array, mask=mask)
        (x, y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+3, y1:y2+3]
        reader = easyocr.Reader(['ar'], gpu=False)
        reader.decoder = 'beamsearch'
        reader.allowlist = '0123456789تونس'
        result = reader.recognize(cropped_image)[0]
        license_plate = result[1]
        # print(result)
        # for element in result:
        #     print(element)
        return license_plate
    
    @staticmethod
    def find_closest_match(result: str, conf_thres=0.5) -> LicensePlate | None:
        '''Returns the closest match in LicensePlates if it exists, else None.'''
        license_plates = LicensePlate.objects.all()
        print(f'Text detected: {result}')
        print(f'License plates: {license_plates}')
        max_score = 0.0
        max_score_index = -1
        print('Starting the process...')
        for index, plate in enumerate(license_plates):
            print(f'*** Iteration {index + 1}:')
            plate_text = plate.plate_text
            print(f' - - Plate text: {plate_text}')
            score = jaro_winkler(result, plate_text)
            print(f' - - Score: {score}')
            if score > max_score:
                print(' - - (New close match!)')
                max_score = score
                print(f' - - Max score: {max_score}')
                max_score_index = index
                print(f' - - Max score index: {max_score_index}')
            print(f' - - Index: {index}')
        if max_score < conf_thres:
            return None
        closest_match = license_plates[max_score_index]
        print(f'Closest match: {closest_match}')
        return closest_match
        

def main():
    from time import process_time
    pr = PlateReader()
    # Getting the result from Theos AI
    theos_ai_start = process_time()
    prediction_data_theos_ai = pr.detect_from_theos_ai()[0]
    # response = json.dumps(prediction_data_theos_ai)
    # print(response)
    license_plate_theos_ai = prediction_data_theos_ai['text']
    print(f'License plate returned from Theos AI: {license_plate_theos_ai}')
    theos_ai_end = process_time()
    theos_ai_time = theos_ai_end - theos_ai_start
    print(f'Execution time: {theos_ai_time:.3f}s')
    # Producing the result natively with OpenCV and EasyOCR
    cv_start = process_time()
    license_plate_cv = pr.read()
    print(f'License plate returned natively with OpenCV and EasyOCR: {license_plate_cv}')
    cv_end = process_time()
    cv_time = cv_end - cv_start
    print(f'Execution time: {cv_time:.3f}s')


if __name__ == '__main__':
    main()
