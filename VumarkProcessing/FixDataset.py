import os
import keyboard
import cv2
import json

# get the JSON and parse it

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

with open("mostOfThem.json", 'r') as f:
        data = json.load(f)

data = list(map(mapDict, data))

for item in data:
    img = cv2.imread(os.path.join('C:\\Users\\Noah\\Documents\\code\\DataSet', data['type'], data['name']))
    for x in range(len(item['picto']) - 1):
        img = cv2.line(img, item['picto'][x], item['picto'][x+1], (0, 255, 0), 20)