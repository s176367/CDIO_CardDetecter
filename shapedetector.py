# Python program to explain cv2.rectangle() method

# importing cv2
import cv2

# path


# Reading an image in default mode
image = cv2.imread('Ressources/172333.jpg')

# Window name in which image is displayed
window_name = 'Image'

# Start coordinate, here (5, 5)
# represents the top left corner of rectangle

# Ending coordinate, here (220, 220)
# represents the bottom right corner of rectangl

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 2

# Using cv2.rectangle() method
# Draw a rectangle with blue line borders of thickness of 2 px
cv2.rectangle(image, (1, 1070), (240, 500), (255, 0, 0), 2)
cv2.rectangle(image, (280, 1070), (520, 500), (255, 0, 0), 2)
cv2.rectangle(image, (560, 1070), (800, 500), (255, 0, 0), 2)
cv2.rectangle(image, (840, 1070), (1080, 500), (255, 0, 0), 2)
cv2.rectangle(image, (1120, 1070), (1360, 500), (255, 0, 0), 2)
cv2.rectangle(image, (1400, 1070), (1640, 500), (255, 0, 0), 2)
cv2.rectangle(image, (1680, 1070), (1918, 500), (255, 0, 0), 2)
cv2.rectangle(image, (700, 1), (1918, 400), (255, 0, 0), 2)
cv2.rectangle(image, (520, 1), (280, 400), (255, 0, 0), 2)
# Displaying the image
cv2.imshow('image', image)


if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
