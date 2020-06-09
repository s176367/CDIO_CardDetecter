import numpy as np
import cv2

font = cv2.FONT_HERSHEY_COMPLEX
img = cv2.imread('opencvSnap.jpg', cv2.IMREAD_COLOR)

img2 = cv2.imread('opencvSnap.jpg', cv2.IMREAD_GRAYSCALE)

blurred = cv2.GaussianBlur(img2, (9, 9), 9)

_, threshold = cv2.threshold(blurred, 50, 60, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))

for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.009 * cv2.arcLength(contour, True), True)

    cv2.drawContours(img, [approx], 0, (0, 255, 0), 5)
    x, y, w, h = cv2.boundingRect(approx)
    print(x,y,w,h)
    n = approx.ravel()
    i = 0

    for j in n:
        if i % 2 == 0:
            x = n[i]
            y = n[i + 1]

            string = str(x) + " " + str(y)

            if i == 0:
                cv2.putText(img, string, (x, y), font, 0.5, (255, 0, 0))
            else:
                cv2.putText(img, string, (x, y), font, 0.5, (0, 255, 0))

            i = i + 1

width, height, = 500, 350
pts1 = np.float32([[243,363], [564, 344], [225,170], [542, 130]])
pts2 = np.float32([[0,0], [width,0], [0, height ], [width, height]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
output = cv2.warpPerspective(img2, matrix, (width,height))

for x in range(0,4):
    cv2.circle(img, (pts1[x][0], pts1[x][1]), 5, (0,0, 255), cv2.FILLED)


scale_percent = 100
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(img, dim, interpolation= cv2.INTER_AREA)
resizedorg = cv2.resize(threshold, dim, interpolation= cv2.INTER_AREA)
cv2.imshow('org', resizedorg)
cv2.imshow('warpedperspective', output)
cv2.imshow('image', resized)


if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()