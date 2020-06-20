import argparse
import cv2
import os
import imutils as imutils
import numpy as np
#from switchForCards import dataForwarding, whileReact, deckpile

framewidth = 1920
frameheight = 1080

ref_point = []
crop = False

cap = cv2.VideoCapture(cv2.CAP_DSHOW + 0)
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


def getContours(img, imgContour, standardimg):
    global counter, string, contours

    # Bare for at vise contures
    contours1, hierachy1 = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imgContour, contours1, -1, (255, 0, 255), 1)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        roiDeck0 = standardimg[1 + 1:400 - 1, 600 + 1:920 - 1]
        roiDeck1 = standardimg[500 + 1:1070 - 1, 1 + 1:240 - 1]
        roiDeck2 = standardimg[500 + 1:1070 - 1, 280 + 1:520 - 1]
        roiDeck3 = standardimg[500 + 1:1070 - 1, 560 + 1:800 - 1]
        roiDeck4 = standardimg[500 + 1:1070 - 1, 840 + 1:1080 - 1]
        roiDeck5 = standardimg[500 + 1:1070 - 1, 1120 + 1:1360 - 1]
        roiDeck6 = standardimg[500 + 1:1070 - 1, 1400 + 1:1640 - 1]
        roiDeck7 = standardimg[500 + 1:1070 - 1, 1680 + 1:1918 - 1]
        roiDiscard = standardimg[1 + 1:400 - 1, 280 + 1:520 - 1]

        decks = [roiDeck0, roiDeck1, roiDeck2, roiDeck3, roiDeck4, roiDeck5, roiDeck6, roiDeck7, roiDiscard]

        i = 0

        j = False

        for x in decks:
            imgBlur = cv2.GaussianBlur(decks[i], (7, 7), 3)

            imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
            threshold1 = 39
            threshold2 = 175
            imgCanny = cv2.Canny(imgGray, threshold1, threshold2)

            kernel = np.ones((5, 5))
            imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
            contours, hierachy = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            # cv2.drawContours(roiDeck1, contours, -1, (255, 0, 255), 1)
            for contour in contours:
                area = cv2.contourArea(contour)
                # areaMin = cv2.getTrackbarPos("area", "parameters")
                areaMin = 40000

                if area > areaMin:
                    peri = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
                    box = np.int0(approx)
                    if len(approx) == 4:

                        counter = counter + 1

                        if box[1][0][1] > box[3][0][1]:
                            pathname = warpPicture(box[2], box[1], box[3], box[0], decks[i])
                            print(pathname)


                        elif box[3][0][1] > box[1][0][1]:
                            pathname = warpPicture(box[1], box[0], box[2], box[3], decks[i])
                            print(pathname)


                    else:
                        x, y, w, h = cv2.boundingRect(approx)
                        cv2.putText(imgContour,
                                    "Antal Corners " + str(len(approx)),
                                    (x + w + 20, y + 85),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.7,
                                    (0, 255, 0), 2)
            i = i + 1



def warpPicture(botRight, botLeft, topRight, topLeft, img):
    width, height, = 400, 400
    pts1 = np.float32([botRight, botLeft, topRight, topLeft])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    output = cv2.warpPerspective(img, matrix, (width, height))
    # checkAfAlle(output)
    print(str(counter))
    cv2.imshow('' + str(counter), output)

    #cv2.imwrite('skiftnavn_' + str(counter) + '.jpg', output)
    #print('warpedPicture' + str(counter+266))
    return checkAfAlle(output)
    #return str('der er blevet taget et billed')


def checkAfkort(img, template):
    img1 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    template1 = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
    #cv2.imshow('tresh1', img1)
    #cv2.imshow('tresh2'+str(counter), template1)

    ret, thresh1 = cv2.threshold(img1, 170, 250, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(template1, 170, 250, cv2.THRESH_BINARY)
    bitwise = cv2.bitwise_xor(thresh1, thresh2)
    #cv2.imshow('tresh1'+str(counter), thresh1)
    #cv2.imshow('tresh2', thresh2)
    #cv2.imshow('bitwise',bitwise)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return (cv2.countNonZero(bitwise))


def checkAfAlle(img):
    path = "templateCards/"
    bestmatch = 10000000000
    pathforCard = ''
    # Iterer igennem alle templates
    for image_path in os.listdir(path):

        # Finder kortet
        input_path = os.path.join(path, image_path)
        template = cv2.imread(input_path)

        nuværendematch = checkAfkort(img, template)
        # Køre checkAfSpecifiktKort
        if nuværendematch < bestmatch:
            pathforCard = input_path.replace('templateCards/', '')
            pathforCard1 = pathforCard.split("_", 1)
            finalstring = pathforCard1[0]
            bestmatch = nuværendematch
    print(bestmatch)
    return finalstring


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
    cv2.rectangle(imgContour, (1000, 1), (1918, 400), (0, 255, 0), 2)
    cv2.rectangle(imgContour, (600, 1), (900, 400), (0, 0, 255), 2)
    cv2.rectangle(imgContour, (520, 1), (280, 400), (255, 0, 0), 2)

    imgBlur = cv2.GaussianBlur(img, (7, 7), 3)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = cv2.getTrackbarPos("Threshold1", "parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "parameters")

    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getContours(imgDil, imgContour, img)

    # imgstack = stackImages(0.8, ([img, imgGray, imgCanny], [imgDil, imgContour, imgWarp]))
    cv2.imshow("result", imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
