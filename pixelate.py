import cv2
import numpy as np

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


def uint8todeg(num):
    return num / 255 * 359

def brown():
    return 2, 2, 2


def pastel(h):
    if h >= 291 or h <= 40:
        return 1, 0, 0
    if 41 <= h <= 90:
        return 0, 1, 0
    if 91 <= h <= 290:
        return 0, 0, 1
    return 0, 0, 0

def brightColour(h):
    if h >= 310 or h <= 25:
        return 3, 0, 0
    if 26 <= h <= 40:
        return 2, 1, 0
    if 41 <= h <= 50:
        return 1, 2, 0
    if 51 <= h <= 70:
        return 0, 3, 0
    if 71 <= h <= 150:
        return 0, 2, 1
    if 151 <= h <= 190:
        return 0, 1, 2
    if 191 <= h <= 270:
        return 0, 0, 3
    if 271 <= h <= 295:
        return 1, 0, 2
    if 296 <= h <= 309:
        return 2, 0, 1
    return 0, 0, 0

def getRYB(h, s, v):
    h = uint8todeg(h)
    s = uint8todeg(s)
    v = uint8todeg(v)
    if v < 30:
        return brown()
    elif s < 30:
        if v > 65:
            return pastel(h)
        else:
            return brown()
    else:
        return brightColour(h)


area = 0
for r in range(ROWS):
    for c in range(COLS):
        for i in range(int(height / ROWS)):
            for j in range(int(width / COLS)):
                avg[r][c] += ogimage[i + (r * int(height / ROWS))][j + (c * int(width / COLS))]
                area += 1
        avg[r][c] = avg[r][c] / area  # divide by area of sub-rectangle
        area = 0
        for i in range(3):
            avg[r][c][i] = min(avg[r][c][i], 255)  # make sure nothing is somehow over 255
            result[r][c][i] = avg[r][c][i]

result = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)

out = open("out.txt", "w")
for i in range(ROWS):
    for j in range(COLS):
        r, y, b = getRYB(result[i][j][0], result[i][j][1], result[i][j][2])
        out.write(str(r) + " " + str(y) + " " + str(b) + ", ")
    out.write('\n')

while 1:
    cv2.imshow("Original Image", ogimage)
    cv2.imshow("Result", result)
    if cv2.waitKey(10) & 0xFF == 27:
        break

out.close()
cv2.destroyAllWindows()
