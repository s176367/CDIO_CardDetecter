import os

import cv2
import numpy as np
from scipy import ndimage

def checkAfSpecifiktKort(img, template):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.70)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
        cv2.imshow('awsd', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return True
    else:
        print("No simmilarity found")
        return False

    cv2.waitKey(0)
    cv2.destroyAllWindows()



def checkAfAlle(img):
    path = "templateCards/"

    # Iterer igennem alle templates
    for image_path in os.listdir(path):

        #Finder kortet
        input_path = os.path.join(path, image_path)
        template = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

        # Køre checkAfSpecifiktKort
        if checkAfSpecifiktKort(img, template) == True:

            path = input_path.replace('templateCards/', '')
            path = path.replace('.PNG', '')
            return path

            break



img = cv2.imread('warpedPicture6.jpg')

print(checkAfAlle(img))
