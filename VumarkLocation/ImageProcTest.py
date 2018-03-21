import cv2
import matplotlib
import numpy as np
import os
from os import path
from matplotlib import pyplot as plt
from ShowImagesMatPlot import show_images

cwd = path.relpath(os.path.dirname(os.path.realpath(__file__)))
#path = path.join(cwd, path.join('images', 'robotview.png'))
path = path.join(cwd, path.join('images', '81.jpg'))
#robotPath = path.join(cwd, 'images', 'robotview.png')

img = cv2.imread(path, 1)
img = cv2.pyrDown(img)
img = cv2.pyrDown(img)
img = cv2.pyrDown(img)
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
rs, bs, gs = cv2.split(colorSpace)

# convert back to RGB
r,g,b = cv2.split(img)

bWeight = np.uint8((np.uint16(r) * (255 - np.uint16(b))) >> 8)
gWeight = np.uint8((np.uint16(r) * (255 - np.uint16(g))) >> 8)
bothWeight = np.uint8((np.uint32(r) * (255 - np.uint32(b)) * (255 - np.uint32(g))) >> 16)

bsWeight = np.uint8((np.uint16(rs) * (255 - np.uint16(bs))) >> 8)
gsWeight = np.uint8((np.uint16(rs) * (255 - np.uint16(gs))) >> 8)
bothSWeight = np.uint8((np.uint32(rs) * (255 - np.uint32(bs)) * (255 - np.uint32(gs))) >> 16)

dilation = cv2.dilate(cv2.Canny(bothSWeight, 50, 250), cv2.getStructuringElement(cv2.MORPH_RECT,(3,3)), iterations = 1)

grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

show_images((img, grey, bWeight, gWeight, bothWeight, bsWeight, gsWeight, bothSWeight, dilation), cols=2, 
    titles=("Original", "Grey", "Blue Weighted", "Green Weighted", "Both Weighted", "Shifted Blue Weighted", "Shifted Green Weighted", "Shifted Both Weighted", "Dilated"))