import cv2
import numpy as np

# Dette project er udarbejdet fra denne vejledning: https://www.youtube.com/watch?v=Fchzk1lDt7Q
# Der er derfor nogle metoder derfra som er taget fra denne hjemmeside fremvist i vejledningsvideoen:
# https://www.murtazahassan.com/real-time-contours-shape-detection/


framewidth = 640
frameheight = 480

cap = cv2.VideoCapture(0)
cap.set(3, framewidth)
cap.set(4, frameheight)

coordinates = []


def empty(a):
    pass


cv2.namedWindow("parameters")
cv2.resizeWindow("parameters", 640, 240)
cv2.createTrackbar("Threshold1", "parameters", 150, 255, empty)
cv2.createTrackbar("Threshold2", "parameters", 255, 255, empty)
cv2.createTrackbar("area", "parameters", 10000, 20000, empty)

threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")

counter = 0

def stackImages(scale, imgArray):  # metode herfra https://www.murtazahassan.com/real-time-contours-shape-detection/
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img, imgContour):
    global counter
    contours, hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)



    for contour in contours:
        area = cv2.contourArea(contour)
        areaMin = cv2.getTrackbarPos("area", "parameters")
        if area > areaMin:
            cv2.drawContours(imgContour, contour, -1, (255, 0, 255), 5)
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

            x, y, w, h = cv2.boundingRect(approx)
            print(x, y, h, w)

            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)

            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)

            if cv2.waitKey(1) & 0xFF == ord('c'):
                counter = counter + 1
                cv2.imwrite('warpedPicture' + str(counter) + '.jpg', imgContour)
                imgstatic = cv2.imread('warpedPicture' + str(counter) + '.jpg')
                coordinates.insert(0, x)
                coordinates.insert(1, y)
                coordinates.insert(2, h)
                coordinates.insert(3, w)
                warpPicture(coordinates[0], coordinates[1], coordinates[2], coordinates[3], imgstatic)



def warpPicture(x, y, w, h, img):
    width, height, = 500, 500
    pts1 = np.float32([[x, y], [x + h, y], [x, y + w], [x + h, y + w]])
    pts2 = np.float32([[0,0], [width,0], [0, height ], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    output = cv2.warpPerspective(img, matrix, (width, height))
    cv2.imshow('warpedPicture' + str(counter), output)


while True:
    success, img = cap.read()

    imgContour = img.copy()
    imgWarp = imgContour.copy()

    imgBlur = cv2.GaussianBlur(img, (7, 7), 3)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("Threshold1", "parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "parameters")

    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getContours(imgDil, imgContour)

    imgstack = stackImages(0.8, ([img, imgGray, imgCanny], [imgDil, imgContour, imgWarp]))
    cv2.imshow("result", imgstack)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
