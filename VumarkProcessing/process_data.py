import json
import os
import cv2
import numpy as np
from ShowImagesMatPlot import show_images
from matplotlib import pyplot as plt
from matplotlib import path
import itertools

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
            item['picto'] = (tempRay[0], tempRay[1], tempRay[3], tempRay[2])
        else:
            item['picto'] = tuple(tempRay)
    else:
        item['picto'] = None
    return item

data = list(map(mapDict, data))

for item in data:
    img = cv2.imread(os.path.join('C:\\Users\\Noah\\Documents\\code\\DataSet', item['type'], item['name']))
    # check mah lines
    if item['picto'] != None:
        for i in range(len(item['picto']) - 1):
            img = cv2.line(img, item['picto'][i], item['picto'][i+1], (0, 255, 0), 20)
        # create path
        p = path.Path(item['picto'])
        print(tuple(itertools.product(*[range(img.shape[1]), range(img.shape[0])])))
        mask = np.matrix(p.contains_points())
        # make a mask using the points given
        

    img = cv2.pyrDown(img)
    img = cv2.pyrDown(img)

    shape = img.shape

    #random = np.random.randint(0, high=255, size=shape, dtype=np.uint8)

    cv2.imshow("sigh", img)

    cv2.waitKey(0)

    cv2.destroyAllWindows()