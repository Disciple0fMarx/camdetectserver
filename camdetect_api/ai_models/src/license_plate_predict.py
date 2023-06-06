import requests
# import json
import cv2
# from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
from PIL import Image
from django.conf import settings


IMAGE_PATH: str = '/home/dhya/Downloads/dataset/mat.jpg'
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


def main():
    from colorama import Fore, Style
    from time import process_time
    pr = PlateReader()
    # Getting the result from Theos AI
    theos_ai_start = process_time()
    prediction_data_theos_ai = pr.detect_from_theos_ai()[0]
    # response = json.dumps(prediction_data_theos_ai)
    # print(response)
    license_plate_theos_ai = prediction_data_theos_ai['text']
    print(f'License plate returned from Theos AI: {Fore.YELLOW}{license_plate_theos_ai}{Style.RESET_ALL}')
    theos_ai_end = process_time()
    theos_ai_time = theos_ai_end - theos_ai_start
    print(f'Execution time: {Fore.BLUE}{theos_ai_time:.3f}s{Style.RESET_ALL}')
    # Producing the result natively with OpenCV and EasyOCR
    cv_start = process_time()
    license_plate_cv = pr.read()
    print(f'License plate returned natively with OpenCV and EasyOCR: {Fore.YELLOW}{license_plate_cv}{Style.RESET_ALL}')
    cv_end = process_time()
    cv_time = cv_end - cv_start
    print(f'Execution time: {Fore.BLUE}{cv_time:.3f}s{Style.RESET_ALL}')


if __name__ == '__main__':
    main()
