import cv2
import numpy as np
import math

ROWS = 30
COLS = 24

ogimage = cv2.imread('image.jpg')
height, width, channels = ogimage.shape
cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
cv2.moveWindow("Original Image", 0, 0)

avg = np.zeros(shape=(ROWS, COLS, 3), dtype=np.uint64)
result = np.zeros(shape=(ROWS, COLS, 3), dtype=np.uint8)

cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
cv2.moveWindow("Result", width, 0)

def magn(r, g, b):
    return math.sqrt(r*r + g*g + b*b)

area = 0
for r in range(ROWS):
    for c in range(COLS):
        for i in range(int(height/ROWS)):
            for j in range(int(width/COLS)):
                avg[r][c] += ogimage[i + (r*int(height/ROWS))][j + (c*int(width/COLS))]
                area+=1
        avg[r][c] = avg[r][c]/area #divide by area of sub-rectangle
        area = 0
        for i in range(3):
            avg[r][c][i] = min(avg[r][c][i], 255) #make sure nothing is somehow over 255
        result[r][c][0] = magn(avg[r][c][0], avg[r][c][1], avg[r][c][2])
        result[r][c][1] = result[r][c][0]
        result[r][c][2] = result[r][c][0]

while 1:
    cv2.imshow("Original Image", ogimage)
    cv2.imshow("Result", result)
    if cv2.waitKey(10) & 0xFF ==27:
        break


cv2.destroyAllWindows()