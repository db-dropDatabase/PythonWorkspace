import json
import os
import cv2
import numpy as np
from ShowImagesMatPlot import show_images
from matplotlib import pyplot as plt

data = ''

with open("first100.json", 'r') as f:
        data = json.load(f)

def mapDict(item):
    str = '[' + item['picto'] + ']'
    ray = json.loads(str)
    item['picto'] = [0, 0, 0, 0]
    if len(ray) > 0:
        for i in range(0, 4):
            item['picto'][i] = [ray[i * 2], ray[i * 2 + 1]]
    return item

map(mapDict, data)

img = cv2.imread(data[0]['name'])
img = cv2.pyrDown(img)
img = cv2.pyrDown(img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


shape = img.shape
print(shape)

random = np.random.randint(0, high=255, size=shape, dtype=np.uint8)

print("Jesus christ")

cv2.imshow("sigh", random)

cv2.waitKey(0)

cv2.destroyAllWindows()