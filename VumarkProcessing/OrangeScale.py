import cv2
import matplotlib
import numpy as np
import os
from os import path
from matplotlib import pyplot as plt
from ShowImagesMatPlot import show_images

cwd = path.relpath(os.path.dirname(os.path.realpath(__file__)))
path = path.join(cwd, path.join('images', 'robotview.png'))
#robotPath = path.join(cwd, 'images', 'robotview.png')

img = cv2.imread(path, 1)
#img = cv2.pyrDown(img)
img = cv2.pyrDown(img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

IMG_SHAPE = img.shape
IMG_WIDTH = IMG_SHAPE[1]
IMG_HEIGHT = IMG_SHAPE[0]

colorSpace = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

# subtract 30 degrees from all hues values
val = 15
for row in colorSpace:
    for pixel in row:
        if(pixel[0] < val):
            pixel[0] = 180 - (val - pixel[0])
        else:
            pixel[0] -= val

colorSpace = cv2.cvtColor(colorSpace, cv2.COLOR_HSV2RGB)
h,s,v = cv2.split(colorSpace)

# convert back to RGB
r,g,b = cv2.split(colorSpace)

satWeight = np.uint8((np.uint16(r) * (255 - np.uint16(s))) >> 8)
valWeight = np.uint8((np.uint16(r) * (255 - np.uint16(v))) >> 8)
bothWeight = np.uint8((np.uint32(r) * (255 - np.uint32(s)) * (255 - np.uint32(v))) >> 16)

grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

show_images((img, colorSpace, r, satWeight, valWeight, bothWeight, grey), cols=2, titles=("Original", "Hue Shifted", "Orange Channel", "Saturation Weighted Orange Channel", "Value Weighted Orange Channel", "Both Weighted Orange Channel", "Greyscale"))