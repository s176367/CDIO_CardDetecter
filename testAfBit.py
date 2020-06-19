# organizing imports
import os

import cv2
import numpy as np

def checkAfkort (img, template):
    img1 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    template1 = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
    # cv2.imshow('tresh1', img1)
    # cv2.imshow('tresh2', template1)

    ret,thresh1 = cv2.threshold(img1, 122, 230, cv2.THRESH_BINARY)
    ret,thresh11 = cv2.threshold(template1, 122, 230, cv2.THRESH_BINARY)
    bitwise = cv2.bitwise_xor(thresh1, thresh11)
    # cv2.imshow('tresh1',thresh1)
    # cv2.imshow('tresh2', thresh11)
    # cv2.imshow('bitwise',bitwise)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    print (cv2.countNonZero(bitwise))
    return (cv2.countNonZero(bitwise))


def checkAfAlle(img):
    path = "templateCards/"
    bestmatch = 10000000000
    pathforCard = ''
    # Iterer igennem alle templates
    for image_path in os.listdir(path):

        #Finder kortet
        input_path = os.path.join(path, image_path)
        template = cv2.imread(input_path)

        nuværendematch = checkAfkort(img, template)
        # Køre checkAfSpecifiktKort
        if nuværendematch < bestmatch:
            pathforCard =  input_path.replace('template/', '')
            bestmatch = nuværendematch
    return bestmatch,pathforCard

img = cv2.imread("warpedPicture92.jpg")

print(checkAfAlle(img))
