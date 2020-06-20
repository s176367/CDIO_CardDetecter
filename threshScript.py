import os

import cv2

path = "templateCards/"
for image_path in os.listdir(path):

    # Finder kortet
    input_path = os.path.join(path, image_path)
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

    ret, threshpic1 = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
    ret, threshpic2 = cv2.threshold(img, 190, 255, cv2.THRESH_BINARY)
    ret, threshpic3 = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)
    ret, threshpic4 = cv2.threshold(img, 160, 255, cv2.THRESH_BINARY)
    ret, threshpic5 = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)
    ret, threshpic6 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    ret, threshpic7 = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

    cv2.imshow('1', threshpic1)
    cv2.imshow('2', threshpic2)
    cv2.imshow('3', threshpic3)
    cv2.imshow('4', threshpic4)
    cv2.imshow('5', threshpic5)
    cv2.imshow('6', threshpic6)
    cv2.imshow('7', threshpic7)


    pathforCard = input_path.replace('templateCards/', '')
    navn = pathforCard


    if cv2.waitKey(0) & 0xFF == ord('1'):
        cv2.imwrite(navn, threshpic1)
        print(navn)


    elif cv2.waitKey(0) & 0xFF == ord('2'):
        cv2.imwrite(navn, threshpic2)
        print(navn)


    elif cv2.waitKey(0) & 0xFF == ord('3'):
        cv2.imwrite(navn, threshpic3)
        print(navn)


    elif cv2.waitKey(0) & 0xFF == ord('4'):
        cv2.imwrite(navn, threshpic4)
        print(navn)


    elif cv2.waitKey(0) & 0xFF == ord('5'):
        cv2.imwrite(navn, threshpic5)
        print(navn)


    elif cv2.waitKey(0) & 0xFF == ord('6'):
        cv2.imwrite(navn, threshpic4)
        print(navn)


    elif cv2.waitKey(0) & 0xFF == ord('7'):
        cv2.imwrite(navn, threshpic5)
        print(navn)




