import cv2
import matplotlib
import numpy as np
import os
from os import path
from matplotlib import pyplot as plt
from ShowImagesMatPlot import show_images
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.widgets import Slider, Button, RadioButtons
from BlobUtil import ExpandingBoxCluster
from BlobUtil import P
from BlobUtil import RayCastClassifier
from BlobUtil import ClockwisePointSort

cwd = path.relpath(os.path.dirname(os.path.realpath(__file__)))
#path = path.join(cwd, path.join('images', 'robotview.png'))
path = path.join(cwd, path.join('images', '81.jpg'))
#robotPath = path.join(cwd, 'images', 'robotview.png')

orgImg = cv2.imread(path, 1)
orgImg = cv2.cvtColor(orgImg, cv2.COLOR_BGR2RGB)
img = cv2.pyrDown(orgImg)
img = cv2.pyrDown(img)
img = cv2.pyrDown(img)
#img = cv2.pyrDown(img)

PYR_COUNT = 3
IMG_SHAPE = img.shape
IMG_WIDTH = IMG_SHAPE[1]
IMG_HEIGHT = IMG_SHAPE[0]

print(IMG_SHAPE)

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

bothSWeight = np.uint8((np.uint32(rs) * (255 - np.uint32(bs)) * (255 - np.uint32(gs))) >> 16)

KERN = np.ones((5,5),np.uint8)

# Start Main
# Create slider for the image rotating
plt.figure()
ax = plt.gca()
imPlot = ax.imshow(cv2.dilate(cv2.Canny(bothSWeight, 50, 250), KERN), cmap="gray")

div = make_axes_locatable(ax)
minVal = Slider(div.append_axes("bottom", size="10%", pad=0.3), "Min", 0, 300, valinit=50)
maxVal = Slider(div.append_axes("bottom", size="10%", pad=0.3), "Max", 0, 500, valinit=250)
cornerThresh = Slider(div.append_axes("top", size="10%", pad=0.3), "Corner Thresh", 0, 2.0, valinit=0.01)

def proc(img):
    org = img.copy()
    img = cv2.dilate(cv2.Canny(bothSWeight, minVal.val, maxVal.val), KERN)
    # look for the largest blob in the left half of the image
    boxes = ExpandingBoxCluster(img, 1, xSearchDist=img.shape[1]>>1)
    # sort by largest y box
    largestY = 0
    index = 0
    for i in range(len(boxes)):
        yDist = boxes[i][P.BOTTOM_RIGHT_Y] - boxes[i][P.TOP_LEFT_Y]
        if yDist > largestY:
            index = i
            largestY = yDist
    # crop image to largest box to just look at pictograph
    img = img[boxes[index][P.TOP_LEFT_Y] - 10:boxes[index][P.BOTTOM_RIGHT_Y] + 10, boxes[index][P.TOP_LEFT_X] - 10:boxes[index][P.BOTTOM_RIGHT_X] + 10]
    xOff = boxes[index][P.TOP_LEFT_X] - 10
    yOff = boxes[index][P.TOP_LEFT_Y] - 10
    drawCorn = img.copy()
    corners = cv2.cornerHarris(img, 3, 5, 0.08)
    totalCorn = 0
    for x in range(drawCorn.shape[0]):
        for y in range(drawCorn.shape[1]):
            if(corners[x,y] >= cornerThresh.val):
                drawCorn[x,y] = 255
            else:
                drawCorn[x,y] = 0

    boxes = ExpandingBoxCluster(drawCorn, 1)

    drawBox = cv2.merge((img, drawCorn, img))

    betterPoints = RayCastClassifier(img, boxes, drawCorn.shape[1] >> 1, drawCorn.shape[0] >> 1, startIter=4)

    #for box in boxes:
    #    cv2.rectangle(drawBox, (box[0], box[1]), (box[2], box[3]), (255, 0, 0))

    # look for lowest and highest x and y value
    largestBox = [drawCorn.shape[1] >> 1, drawCorn.shape[0] >> 1, drawCorn.shape[1] >> 1, drawCorn.shape[0] >> 1]
    for box in betterPoints[0]:
        for i in range(2):
            # check x
            x = box[i*2]
            if x < largestBox[P.TOP_LEFT_X]:
                largestBox[P.TOP_LEFT_X] = x
            elif x > largestBox[P.BOTTOM_RIGHT_X]:
                largestBox[P.BOTTOM_RIGHT_X] = x
            # check y
            y = box[i*2+1]
            if y < largestBox[P.TOP_LEFT_Y]:
                largestBox[P.TOP_LEFT_Y] = y
            elif y > largestBox[P.BOTTOM_RIGHT_Y]:
                largestBox[P.BOTTOM_RIGHT_Y] = y
    # add previously cropped offsets back into the image
    largestBox[P.TOP_LEFT_X] += xOff
    largestBox[P.BOTTOM_RIGHT_X] += xOff
    largestBox[P.TOP_LEFT_Y] += yOff
    largestBox[P.BOTTOM_RIGHT_Y] += yOff
    # crop image to largest box, and display it
    
    polyPoints = ClockwisePointSort((drawCorn.shape[1] >> 1, drawCorn.shape[0] >> 1), map(lambda p: (p[0], p[1]), betterPoints[0]))

    leng = len(polyPoints)
    for i in range(leng):
        cv2.drawMarker(drawBox, polyPoints[i], ((255 / leng) * i, (255 / leng) * (leng - i - 1)), markerSize=2)
    
    for box in betterPoints[1]:
        cv2.rectangle(drawBox, (box[0], box[1]), (box[2], box[3]), (255, 165, 0))
    
    cv2.drawMarker(drawBox, (drawCorn.shape[1] >> 1, drawCorn.shape[0] >> 1), (255, 0, 0))

    return drawBox
    
    # de-pyramid coordinated
    """
    for i in range(len(largestBox)):
        largestBox[i] *= pow(2, PYR_COUNT)
    return orgImg[largestBox[P.TOP_LEFT_Y]:largestBox[P.BOTTOM_RIGHT_Y], largestBox[P.TOP_LEFT_X]:largestBox[P.BOTTOM_RIGHT_X]]
    """

update = lambda x: imPlot.set_data(proc(bothSWeight))
minVal.on_changed(update)
maxVal.on_changed(update)
cornerThresh.on_changed(update)

plt.show()