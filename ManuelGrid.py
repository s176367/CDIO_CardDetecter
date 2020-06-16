import cv2





img = cv2.imread('Ressources/172333.jpg', cv2.COLOR_RGB2GRAY)
cv2.rectangle(img, (1, 1070), (240, 500), (255, 0, 0), 2)
cv2.rectangle(img, (280, 1070), (520, 500), (255, 0, 0), 2)
cv2.rectangle(img, (560, 1070), (800, 500), (255, 0, 0), 2)
cv2.rectangle(img, (840, 1070), (1080, 500), (255, 0, 0), 2)
cv2.rectangle(img, (1120, 1070), (1360, 500), (255, 0, 0), 2)
cv2.rectangle(img, (1400, 1070), (1640, 500), (255, 0, 0), 2)
cv2.rectangle(img, (1680, 1070), (1918, 500), (255, 0, 0), 2)
cv2.rectangle(img, (520, 1), (280, 400), (255, 0, 0), 2)
# cv2.rectangle(img, (700, 1), (1918, 400), (255, 0, 0), 2)


roiDeck1 = img[500+1:1070-1, 1+1:240-1]
roiDeck2 = img[500+1:1070-1, 280+1:520-1]
roiDeck3 = img[500+1:1070-1, 560+1:800-1]
roiDeck4 = img[500+1:1070-1, 840+1:1080-1]
roiDeck5 = img[500+1:1070-1, 1120+1:1360-1]
roiDeck6 = img[500+1:1070-1, 1400+1:1640-1]
roiDeck7 = img[500+1:1070-1, 1680+1:1918-1]
roiDiscard = img[1+1:400-1, 280+1:520-1]
# roiDeck8 = img[400:1070-1, 700:1918]


# cv2.imshow('ROI',roiDeck1)
# cv2.imshow('ROI2',roiDeck2)
# cv2.imshow('ROI3',roiDeck3)
# cv2.imshow('ROI4',roiDeck4)
# cv2.imshow('ROI5',roiDeck5)
# cv2.imshow('ROI7',roiDeck6)
# cv2.imshow('ROI6',roiDeck7)
cv2.imshow('2',roiDiscard)
# cv2.imshow('ROI3',roiDeck9)





cv2.imshow('g', img)

cv2.waitKey(0)
cv2.destroyAllWindows()
