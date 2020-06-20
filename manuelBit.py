import cv2



img = cv2.imread('templateBinary/8_12.jpg', cv2.IMREAD_GRAYSCALE)
template = cv2.imread('templateBinary/6_8.jpg', cv2.IMREAD_GRAYSCALE)
template1 = cv2.imread('templateBinary/6_9.jpg', cv2.IMREAD_GRAYSCALE)


cv2.imshow('template',template)
cv2.imshow('img',img)
cv2.imshow('testpicture',template1)

bitwise = cv2.bitwise_xor(template, img)
bitwise1 = cv2.bitwise_xor(template, template1)

cv2.imshow('Bitwise xor', bitwise)
cv2.imshow('Bitwise xor2', bitwise)

# cv2.imshow('Queen', threshpic8)
# cv2.imshow('Queen2', threshpic7)
# cv2.imshow('Ace', threshpic153)

cv2.waitKey(0)
cv2.destroyAllWindows()

print(cv2.countNonZero(bitwise))
print(cv2.countNonZero(bitwise1))


# print (cv2.sumElems(dest_and)[0])

