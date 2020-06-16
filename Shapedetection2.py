import argparse
import cv2
import os
import imutils as imutils
import numpy as np

# Dette project er udarbejdet fra denne vejledning: https://www.youtube.com/watch?v=Fchzk1lDt7Q
# Der er derfor nogle metoder derfra som er taget fra denne hjemmeside fremvist i vejledningsvideoen:
# https://www.murtazahassan.com/real-time-contours-shape-detection/


framewidth = 1920
frameheight = 1080

ref_point = []
crop = False

cap = cv2.VideoCapture(cv2.CAP_DSHOW )
cap.set(cv2.CAP_PROP_FRAME_WIDTH, framewidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameheight)




coordinates = []


def empty(a):
    pass


cv2.namedWindow("parameters")
cv2.resizeWindow("parameters", 640, 240)
cv2.createTrackbar("Threshold1", "parameters", 150, 255, empty)
cv2.createTrackbar("Threshold2", "parameters", 255, 255, empty)
cv2.createTrackbar("area", "parameters", 10000, 20000, empty)
cv2.createTrackbar("maxArea", "parameters", 20000, 20000, empty)

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


def getContours(img, imgContour, standardimg):
    global counter, string

    roiDeck1 = img[500 + 1:1070 - 1, 1 + 1:240 - 1]
    roiDeck2 = img[500 + 1:1070 - 1, 280 + 1:520 - 1]
    roiDeck3 = img[500 + 1:1070 - 1, 560 + 1:800 - 1]
    roiDeck4 = img[500 + 1:1070 - 1, 840 + 1:1080 - 1]
    roiDeck5 = img[500 + 1:1070 - 1, 1120 + 1:1360 - 1]
    roiDeck6 = img[500 + 1:1070 - 1, 1400 + 1:1640 - 1]
    roiDeck7 = img[500 + 1:1070 - 1, 1680 + 1:1918 - 1]
    roiDiscard = img[1 + 1:400 - 1, 280 + 1:520 - 1]
    decks = [roiDeck1,roiDeck2,roiDeck3,roiDeck3,roiDeck4,roiDeck5,roiDeck6,roiDeck7,roiDiscard]

    for x in decks:
        contours, hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(imgContour, contours, -1, (255, 0, 255), 3)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        for x in decks:
            for contour in contours:
                area = cv2.contourArea(contour)
                areaMin = cv2.getTrackbarPos("area", "parameters")

                if area > areaMin:
                    peri = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
                    box = np.int0(approx)

                    if len(approx) == 4:
                        x, y, w, h = cv2.boundingRect(approx)

                        # cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX,
                        # 0.7, (0, 255, 0), 2)
                        # cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        #        (0, 255, 0), 2)


                        counter = counter + 1
                        print(box)
                        imgstatic = cv2.imread('warpedPicture' + str(counter) + '.jpg')
                        coordinates.insert(0, x)
                        coordinates.insert(1, y)
                        coordinates.insert(2, h)
                        coordinates.insert(3, w)
                        warpPic = standardimg.copy()
                        warpPicture(box[0], box[1], box[2], box[3], warpPic)

                    else:
                        x, y, w, h = cv2.boundingRect(approx)
                        cv2.putText(imgContour,
                                    "Ret kort indtil",
                                    (x + w + 20, y + 20),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                    (0, 255, 0), 2)
                        cv2.putText(imgContour,
                                    "green firkant vises ",
                                    (x + w + 20, y + 45),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                    (0, 255, 0), 2)
                        cv2.putText(imgContour,
                                    "MAKS 4 Corners ",
                                    (x + w + 20, y + 65),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                    (0, 255, 0), 2)
                        cv2.putText(imgContour,
                                    "Antal Corners " + str(len(approx)),
                                    (x + w + 20, y + 85),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                    (0, 255, 0), 2)


def warpPicture(y, x , w, h, img):
    width, height, = 400, 400
    pts1 = np.float32([x, y, w, h])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    output = cv2.warpPerspective(img, matrix, (width, height))
    #checkAfAlle(output)
    #print(checkAfAlle(output))
    #cv2.imwrite('warpedPicture' + str(counter) + '.jpg', output)

    cv2.imshow('warpedPicture' + str(counter), output)


def checkAfSpecifiktKort(img, template):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    w, h = template.shape[::-1]
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= 0.85)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
        return True
    else:
        print("No simmilarity found")
        return False

    cv2.waitKey(0)
    cv2.destroyAllWindows()



def checkAfAlle(img):
    path = "templateCards/"

    # Iterer igennem alle templates
    for image_path in os.listdir(path):

        #Finder kortet
        input_path = os.path.join(path, image_path)
        template = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

        # Køre checkAfSpecifiktKort
        if checkAfSpecifiktKort(img, template) == True:
            path = input_path.replace('templateCards/', '')
            path = path.replace('.PNG', '')
            return path
            break

while True:
    success, img = cap.read()
    imgContour = img.copy()
    imgWarp = imgContour.copy()
    cv2.rectangle(img, (1, 1070), (240, 500), (255, 0, 0), 2)
    cv2.rectangle(img, (280, 1070), (520, 500), (255, 0, 0), 2)
    cv2.rectangle(img, (560, 1070), (800, 500), (255, 0, 0), 2)
    cv2.rectangle(img, (840, 1070), (1080, 500), (255, 0, 0), 2)
    cv2.rectangle(img, (1120, 1070), (1360, 500), (255, 0, 0), 2)
    cv2.rectangle(img, (1400, 1070), (1640, 500), (255, 0, 0), 2)
    cv2.rectangle(img, (1680, 1070), (1918, 500), (255, 0, 0), 2)
    cv2.rectangle(img, (700, 1), (1918, 400), (255, 0, 0), 2)
    cv2.rectangle(img, (520, 1), (280, 400), (255, 0, 0), 2)



    imgBlur = cv2.GaussianBlur(img, (7, 7), 3)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    #threshold1 = cv2.getTrackbarPos("Threshold1", "parameters")
    #threshold2 = cv2.getTrackbarPos("Threshold2", "parameters")

    imgCanny = cv2.Canny(imgGray, 120, 120)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getContours(imgDil, imgContour, img)

    #imgstack = stackImages(0.8, ([img, imgGray, imgCanny], [imgDil, imgContour, imgWarp]))
    cv2.imshow("result", imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
