import os

import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('templateCards/warpedPicture29.jpg', 0)  # queryImage
template = cv2.imread('templateCards/warpedPicture7.jpg', 0)  # trainImage
# Initiate SIFT detector
print(template)
orb = cv2.ORB_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(template, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)  # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params, search_params)

des1 = np.float32(des1)
des2 = np.float32(des2)

matches = flann.knnMatch(des1, des2, k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0, 0] for i in range(len(matches))]

# ratio test as per Lowe's paper
count = 0
for i, (m, n) in enumerate(matches):
    if m.distance < 0.9 * n.distance:
        matchesMask[i] = [1, 0]
        count = count + 1

draw_params = dict(matchColor=(0, 255, 0),
                   singlePointColor=(255, 0, 0),
                   matchesMask=matchesMask,
                   flags=0)

img3 = cv2.drawMatchesKnn(img1, kp1, template, kp2, matches, None, **draw_params)

plt.imshow(img3, ), plt.show()

