import json
import os
import cv2
import numpy as np
from ShowImagesMatPlot import show_images
from matplotlib import pyplot as plt
from matplotlib import path
import itertools
import collections

# Resolution 330x270
X_RES = 350
Y_RES = 270

POINTS = np.float32(((0, Y_RES), (0, 0), (X_RES, 0), (X_RES, Y_RES)))

def get_image_from_data(data):
    return cv2.imread(os.path.join('C:\\Users\\Noah\\Documents\\code\\DataSet', data['type'], data['name']))

def scale_points(points, scale):
    return ((points[0][0] - points[0][0] * scale, points[0][1] * (1 + scale)),
            (points[1][0] - points[1][0] * scale, points[1][1] - points[1][1] * scale),
            (points[2][0] * (1 + scale), points[2][1] - points[2][1] * scale),
            (points[3][0] * (1 + scale), points[0][1] * (1 + scale)))

data = ''

with open("first100.json", 'r') as f:
        data = json.load(f)

def mapDict(item):
    str = '[' + item['picto'] + ']'
    ray = json.loads(str)
    tempRay = [0, 0, 0, 0]
    # map flat string to coordinate arrays
    if len(ray) > 0:
        for i in range(0, 4):
            tempRay[i] = (ray[i * 2], ray[i * 2 + 1])
        # sort by X coordinate
        tempRay.sort(key=lambda coord: coord[0])
        # if Y of point 0 is greater than Y of point 1 and the opposite is true of the Y's of the next two points, switch em
        # also vice versa
        if (tempRay[0][1] > tempRay[1][1] and tempRay[2][1] > tempRay[3][1]) or (tempRay[0][1] < tempRay[1][1] and tempRay[2][1] < tempRay[3][1]):
            tempRay = (tempRay[0], tempRay[1], tempRay[3], tempRay[2])
        # switch points so origin is always a bottom left
        if tempRay[0][1] < tempRay[1][1]:
            item['picto'] = (tempRay[1], tempRay[0], tempRay[3], tempRay[2])
        else:
            item['picto'] = tempRay

    else:
        item['picto'] = None
    return item

data = list(map(mapDict, data))

for i in range(len(data)):
    item = data[i]
    img = get_image_from_data(item)
    nextImg = get_image_from_data(data[i+1])
    # check mah lines
    if hasattr(item['picto'], "__len__") and hasattr(data[i+1]['picto'], "__len__"):
        #for x in range(len(item['picto']) - 1):
        #    img = cv2.line(img, item['picto'][x], item['picto'][x+1], (0, 255, 0), 20)

        # warp pictograph of previous into position of next
        pers = cv2.getPerspectiveTransform(np.float32(item['picto']), np.float32(data[i+1]['picto']))
        img = cv2.warpPerspective(img, pers, (nextImg.shape[1], nextImg.shape[0]))

        # warp four point mask matrix to respective points
        pers = cv2.getPerspectiveTransform(np.float32(((0, 0), (0, nextImg.shape[0]), (nextImg.shape[1], nextImg.shape[0]), (nextImg.shape[1], 0))), np.float32(data[i+1]['picto']))
        mask = cv2.warpPerspective(np.full((nextImg.shape[0], nextImg.shape[1]), 255, dtype=np.uint8), pers, (nextImg.shape[1], nextImg.shape[0]))

        # bitwise copy
        img = cv2.bitwise_or(cv2.bitwise_or(0, nextImg, mask=cv2.bitwise_not(mask)), cv2.bitwise_or(0, img, mask=mask))

    img = cv2.pyrDown(img)
    img = cv2.pyrDown(img)

    shape = img.shape

    #random = np.random.randint(0, high=255, size=shape, dtype=np.uint8)

    cv2.imshow("sigh", img)

    cv2.waitKey(0)

    cv2.destroyAllWindows()