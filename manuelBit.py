import cv2



img = cv2.imread('templateCards/warpedpicture375.jpg', cv2.IMREAD_GRAYSCALE)
template = cv2.imread('templateCards/warpedpicture166.jpg', cv2.IMREAD_GRAYSCALE)
template1 = cv2.imread('templateCards/warpedpicture377.jpg', cv2.IMREAD_GRAYSCALE)

cv2.imshow('template', template)

ret,threshpic8 = cv2.threshold(img,170, 255,cv2.THRESH_BINARY)
ret,threshpic7 = cv2.threshold(template, 170, 255, cv2.THRESH_BINARY)
ret,threshpic153 = cv2.threshold(template1,170, 255,cv2.THRESH_BINARY)

cv2.imshow('template',threshpic7)
cv2.imshow('img',threshpic8)
cv2.imshow('testpicture',threshpic153)

bitwise = cv2.bitwise_xor(threshpic8, threshpic7)
bitwise1 = cv2.bitwise_xor(threshpic7, threshpic153)


cv2.imshow('Bitwise xor', bitwise)
cv2.imshow('Bitwise xor2', bitwise1)

# cv2.imshow('Queen', threshpic8)
# cv2.imshow('Queen2', threshpic7)
# cv2.imshow('Ace', threshpic153)

cv2.waitKey(0)
cv2.destroyAllWindows()

print(cv2.countNonZero(bitwise))
print(cv2.countNonZero(bitwise1))
print ('Queen and Queen', cv2.sumElems(bitwise[0])[0])
print ('Queen and ace', cv2.sumElems(bitwise1[0])[0])

# print (cv2.sumElems(dest_and)[0])

