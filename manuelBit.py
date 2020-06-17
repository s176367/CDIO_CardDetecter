import cv2



img = cv2.imread('warpedPicture92.jpg', cv2.IMREAD_GRAYSCALE)
template = cv2.imread('templateCards/warpedPicture93.jpg', cv2.IMREAD_GRAYSCALE)
template1 = cv2.imread('templateCards/warpedPicture100.jpg', cv2.IMREAD_GRAYSCALE)

ret,threshpic8 = cv2.threshold(img,122, 255,cv2.THRESH_BINARY)
ret,threshpic7 = cv2.threshold(template,122, 255,cv2.THRESH_BINARY)
ret,threshpic153 = cv2.threshold(template1,122, 255,cv2.THRESH_BINARY)

cv2.imshow('162',threshpic7)
cv2.imshow('92',threshpic8)
cv2.imshow('ace',threshpic153)

bitwise = cv2.bitwise_xor(threshpic8, threshpic7)
bitwise1 = cv2.bitwise_xor(threshpic8, threshpic153)


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

