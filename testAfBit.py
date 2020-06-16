# organizing imports
import os

import cv2
import numpy as np

def checkAfkort (img, template):
    img1 = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
    template1 = cv2.cvtColor(template, cv2.IMREAD_GRAYSCALE)
    ret,thresh1 = cv2.threshold(img1, 110, 255, cv2.THRESH_BINARY)
    ret,thresh11 = cv2.threshold(template1, 110, 255, cv2.THRESH_BINARY)

    print (cv2.sumElems(cv2.subtract(thresh1, thresh11))[0])
    return (cv2.sumElems(cv2.subtract(thresh1,thresh11))[0])


def checkAfAlle(img):
    path = "templateCards/"
    bestmatch = 100000000000000000
    pathforCard = ''
    # Iterer igennem alle templates
    for image_path in os.listdir(path):

        #Finder kortet
        input_path = os.path.join(path, image_path)
        template = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

        nuværendematch = checkAfkort(img, template)
        # Køre checkAfSpecifiktKort
        if nuværendematch < bestmatch:
            pathforCard =  input_path.replace('templateCards/', '')
            bestmatch = nuværendematch
    return bestmatch,pathforCard





img = cv2.imread("warpedPicture8.jpg")

print(checkAfAlle(img))
#718335
#2054790
#31243380