import cv2



img = cv2.imread('warpedPicture8.jpg', cv2.IMREAD_GRAYSCALE)


template = cv2.imread('templateCards/warpedPicture7.jpg', cv2.IMREAD_GRAYSCALE)

template1 = cv2.imread('templateCards/warpedPicture153.jpg', cv2.IMREAD_GRAYSCALE)

ret,threshpic8 = cv2.threshold(img,122, 255,cv2.THRESH_BINARY)
ret,threshpic7 = cv2.threshold(template,122, 255,cv2.THRESH_BINARY)
ret,threshpic153 = cv2.threshold(template1,122, 255,cv2.THRESH_BINARY)

dest_and = cv2.bitwise_and(threshpic8, threshpic7)

cv2.imshow('Bitwise And', dest_and)



cv2.imshow('pic8', threshpic8)
cv2.imshow('pic7', threshpic7)
cv2.imshow('pic153', threshpic153)

cv2.waitKey(0)
cv2.destroyAllWindows()

print (cv2.sumElems(cv2.subtract(threshpic8, dest_and))[0])
print (cv2.sumElems(dest_and)[0])
print (cv2.sumElems(cv2.subtract(threshpic8, threshpic153))[0])
