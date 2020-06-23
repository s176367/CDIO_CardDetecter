import cv2



img = cv2.imread('templateCards/15_17261.jpg', cv2.IMREAD_GRAYSCALE)
template = cv2.imread('templateCards/15_18772.jpg', cv2.IMREAD_GRAYSCALE)
template1 = cv2.imread('templateCards/15_17261.jpg', cv2.IMREAD_GRAYSCALE)

ret, thresh1 = cv2.threshold(img, 170, 250, cv2.THRESH_BINARY)
ret, thresh2 = cv2.threshold(template, 170, 250, cv2.THRESH_BINARY)
ret, thresh3 = cv2.threshold(template1, 170, 250, cv2.THRESH_BINARY)


cv2.imshow('template',thresh1)
cv2.imshow('img', thresh2)
cv2.imshow('testpicture',thresh3)

bitwise = cv2.bitwise_xor(template, img)
bitwise1 = cv2.bitwise_xor(template, template1)

cv2.imshow('Bitwise xor', bitwise)
cv2.imshow('Bitwise xor2', bitwise1)

# cv2.imshow('Queen', threshpic8)
# cv2.imshow('Queen2', threshpic7)
# cv2.imshow('Ace', threshpic153)

cv2.waitKey(0)
cv2.destroyAllWindows()

print(cv2.countNonZero(bitwise))
print(cv2.countNonZero(bitwise1))


# print (cv2.sumElems(dest_and)[0])

