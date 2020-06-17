import os

import numpy as np
import cv2
from matplotlib import pyplot as plt

def checkAfkort(img1,template):


    orb = cv2.ORB_create()


    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(template,None)


    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params,search_params)

    des1 = np.float32(des1)
    des2 = np.float32(des2)

    matches = flann.knnMatch(des1,des2,k=2)


    matchesMask = [[0,0] for i in range(len(matches))]

    # ratio test as per Lowe's paper
    count = 0
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.6*n.distance:
            matchesMask[i]=[1,0]
            count = count+1

    # draw_params = dict(matchColor=(0, 255, 0),
    #                    singlePointColor=(255, 0, 0),
    #                    matchesMask=matchesMask,
    #                    flags=0)
    #
    # img3 = cv2.drawMatchesKnn(img1, kp1, template, kp2, matches, None, **draw_params)
    #
    # plt.imshow(img3, ), plt.show()

    return count



def checkAfAlle(img):
    path = "templatesYes/"
    bestmatch = 0
    pathforCard = ''
    # Iterer igennem alle templates
    for image_path in os.listdir(path):

        #Finder kortet
        input_path = os.path.join(path, image_path)
        template = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

        nuværendematch = checkAfkort(img, template)
        # Køre checkAfSpecifiktKort
        if nuværendematch > bestmatch:
            pathforCard =  input_path.replace('templateCards/', '')
            bestmatch = nuværendematch
    return bestmatch,pathforCard





img = cv2.imread("Ressources/warpedPicture42.jpg")

print(checkAfAlle(img))
