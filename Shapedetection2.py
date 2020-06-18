import argparse
import cv2
import os
import imutils as imutils
import numpy as np
from operator import itemgetter

# Dette project er udarbejdet fra denne vejledning: https://www.youtube.com/watch?v=Fchzk1lDt7Q
# Der er derfor nogle metoder derfra som er taget fra denne hjemmeside fremvist i vejledningsvideoen:
# https://www.murtazahassan.com/real-time-contours-shape-detection/


framewidth = 1920
frameheight = 1080

ref_point = []
crop = False

cap = cv2.VideoCapture(cv2.CAP_DSHOW+1)
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
    global counter, string, contours

    roiDeck1 = img[500 + 1:1070 - 1, 1 + 1:240 - 1]
    roiDeck2 = img[500 + 1:1070 - 1, 280 + 1:520 - 1]
    roiDeck3 = img[500 + 1:1070 - 1, 560 + 1:800 - 1]
    roiDeck4 = img[500 + 1:1070 - 1, 840 + 1:1080 - 1]
    roiDeck5 = img[500 + 1:1070 - 1, 1120 + 1:1360 - 1]
    roiDeck6 = img[500 + 1:1070 - 1, 1400 + 1:1640 - 1]
    roiDeck7 = img[500 + 1:1070 - 1, 1680 + 1:1918 - 1]
    roiDiscard = img[1 + 1:400 - 1, 280 + 1:520 - 1]
    decks = [roiDeck1,roiDeck2,roiDeck3,roiDeck3,roiDeck4,roiDeck5,roiDeck6,roiDeck7,roiDiscard]

    #for x in decks:
    contours, hierachy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imgContour, contours, -1, (255, 0, 255), 1)

    if cv2.waitKey(1) & 0xFF == ord('c'):

         #for x in decks:
            for contour in contours:
                area = cv2.contourArea(contour)
                areaMin = cv2.getTrackbarPos("area", "parameters")

                if area > areaMin:
                    peri = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
                    box = np.int0(approx)




                    if len(approx) == 4:
                        counter = counter + 1
                        warpPic = standardimg.copy()
                        if box[1][0][1]> box[3][0][1]:
                            warpPicture(box[2], box[1], box[3], box[0], warpPic)

                        elif box[3][0][1] > box[1][0][1]:
                            warpPicture(box[1], box[0], box[2], box[3], warpPic)


                    else:
                        x, y, w, h = cv2.boundingRect(approx)
                        cv2.putText(imgContour,
                                    "Antal Corners " + str(len(approx)),
                                    (x + w + 20, y + 85),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                    (0, 255, 0), 2)


def warpPicture(botRight, botLeft, topRight, topLeft, img):
    width, height, = 400, 400
    pts1 = np.float32([botRight, botLeft, topRight, topLeft])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    output = cv2.warpPerspective(img, matrix, (width, height))
    #checkAfAlle(output)
    print(str(counter))
    #print(checkAfAlle(output))
    # cv2.imshow(''+ str(counter), output)
    cv2.imwrite('warpedpicture' + str(counter) + '.jpg', output)
    #print('warpedPicture' + str(counter))


def antiflip(box):
    # y1 = box[0][0][1]
    # y2 = box[1][0][1]
    # y3 = box[2][0][1]
    # y4 = box[3][0][1]
    cord1 = box[0][0]
    cord2 = box[1][0]
    cord3 = box[2][0]
    cord4 = box[3][0]

    ycords = [cord1[1], cord2[1], cord3[1], cord4[1]]
    ycords.index(max(ycords))
    rækkefølgeUdfraY = [box[ycords.index(max(ycords))]]
    ycords.remove(max(ycords))
    rækkefølgeUdfraY.append(box[ycords.index(max(ycords))])
    ycords.remove(max(ycords))
    rækkefølgeUdfraY.append(box[ycords.index(max(ycords))])
    ycords.remove(max(ycords))
    rækkefølgeUdfraY.append(box[ycords.index(max(ycords))])

    return rækkefølgeUdfraY



def checkAfkort (img, template):
    img1 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    template1 = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
    # cv2.imshow('tresh1', img1)
    # cv2.imshow('tresh2', template1)

    ret,thresh1 = cv2.threshold(img1, 190, 230, cv2.THRESH_BINARY)
    ret,thresh11 = cv2.threshold(template1, 190, 230, cv2.THRESH_BINARY)
    bitwise = cv2.bitwise_xor(thresh1, thresh11)
    # cv2.imshow('tresh1',thresh1)
    # cv2.imshow('tresh2', thresh11)
    # cv2.imshow('bitwise',bitwise)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return (cv2.countNonZero(bitwise))


def checkAfAlle(img):
    path = "templateCards/"
    bestmatch = 10000000000
    pathforCard = ''
    # Iterer igennem alle templates
    for image_path in os.listdir(path):

        #Finder kortet
        input_path = os.path.join(path, image_path)
        template = cv2.imread(input_path)

        nuværendematch = checkAfkort(img, template)
        # Køre checkAfSpecifiktKort
        if nuværendematch < bestmatch:
            pathforCard =  input_path.replace('test/', '')
            bestmatch = nuværendematch
    return bestmatch,pathforCard

while True:
    success, img = cap.read()
    imgContour = img.copy()
    imgWarp = imgContour.copy()
    cv2.rectangle(imgContour, (1, 1070), (240, 500), (255, 0, 0), 2)
    cv2.rectangle(imgContour, (280, 1070), (520, 500), (255, 0, 0), 2)
    cv2.rectangle(imgContour, (560, 1070), (800, 500), (255, 0, 0), 2)
    cv2.rectangle(imgContour, (840, 1070), (1080, 500), (255, 0, 0), 2)
    cv2.rectangle(imgContour, (1120, 1070), (1360, 500), (255, 0, 0), 2)
    cv2.rectangle(imgContour, (1400, 1070), (1640, 500), (255, 0, 0), 2)
    cv2.rectangle(imgContour, (1680, 1070), (1918, 500), (255, 0, 0), 2)
    cv2.rectangle(imgContour, (700, 1), (1918, 400), (255, 0, 0), 2)
    cv2.rectangle(imgContour, (520, 1), (280, 400), (255, 0, 0), 2)



    imgBlur = cv2.GaussianBlur(img, (7, 7), 3)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = cv2.getTrackbarPos("Threshold1", "parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "parameters")

    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getContours(imgDil, imgContour, img)


    #imgstack = stackImages(0.8, ([img, imgGray, imgCanny], [imgDil, imgContour, imgWarp]))
    cv2.imshow("result", imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
