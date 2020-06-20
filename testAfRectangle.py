
import cv2



img = cv2.imread('backround.jpg')

# cv2.rectangle(img, (1, 1070), (240, 500), (255, 0, 0), 2)
# cv2.rectangle(img, (280, 1070), (520, 500), (255, 0, 0), 2)
# cv2.rectangle(img, (560, 1070), (800, 500), (255, 0, 0), 2)
# cv2.rectangle(img, (840, 1070), (1080, 500), (255, 0, 0), 2)
# cv2.rectangle(img, (1120, 1070), (1360, 500), (255, 0, 0), 2)
# cv2.rectangle(img, (1400, 1070), (1640, 500), (255, 0, 0), 2)
# cv2.rectangle(img, (1680, 1070), (1918, 500), (255, 0, 0), 2)
# cv2.rectangle(img, (700, 1), (1918, 400), (255, 0, 0), 2)
# cv2.rectangle(img, (520, 1), (280, 400), (255, 0, 0), 2)
roiDiscard = img[1 + 1:400 - 1, 280 + 1:520 - 1]
roiDeck0 = img[1 + 1:400 - 1, 600 + 1:880 - 1]


cv2.imshow('test', img)
cv2.imshow('tes2t', roiDeck0)
cv2.waitKey(0)
cv2.destroyAllWindows()