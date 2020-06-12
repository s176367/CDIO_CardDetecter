import cv2
import numpy as np


def diff(image1, image2):
     return abs(image1-image2).mean()

#HENTER, CROPPER OG LAVER BILLEDERNE BINÆRER
img1 = cv2.imread("Ressources/adiamond.PNG", cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread("Ressources/adiamond2.PNG", cv2.IMREAD_GRAYSCALE)
img3 = cv2.imread("Ressources/aclubs.PNG", cv2.IMREAD_GRAYSCALE)
img4 = cv2.imread("Ressources/aspades.PNG", cv2.IMREAD_GRAYSCALE)
cards = [img1, img2, img3, img4]
binaryCards = []
i = 0
thresh = 127

print(img1.shape)
print(img3.shape)


for x in cards:
    imgcrop = cards[i][0:115, 0:60]
    (thresh, im_bw2) = cv2.threshold(imgcrop, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    im_bw2 = cv2.threshold(imgcrop, thresh, 255, cv2.THRESH_BINARY)[1]
    binaryCards.append(im_bw2)
    i = i+1;

#BITWISE OPERATION 'AND' FOR AT SAMMENSÆTTE DE KORT SOM BLIVER SAMMENLIGNET
bitAnd = cv2.bitwise_and(binaryCards[0], binaryCards[3])

#SÆTTER BILLEDERNE TIL FLOATS; SÅ DE KAN SAMMENLIGNETS MED DIFF METODEN
# print(bitAnd)
# print(binaryCards[0])
# print(binaryCards[1])
img0 = binaryCards[0].astype(float)
img1 = binaryCards[3].astype(float)
print(diff(img0, img1))

#cv2.imshow("Hejasd", bitAnd)
cv2.imshow("hej",binaryCards[0])
cv2.imshow("hej2",binaryCards[3])
# cv2.imshow("hej3",binaryCards[2])
# cv2.imshow("hej4",binaryCards[3])

cv2.waitKey(0)
cv2.destroyAllWindows()

