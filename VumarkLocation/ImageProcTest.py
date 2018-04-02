import cv2
import matplotlib
import numpy as np
import os
from os import path
from matplotlib import pyplot as plt
from ShowImagesMatPlot import show_images

def process(img):
    colorSpace = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    # subtract 30 degrees from all hues values
    val = 15
    for row in colorSpace:
        for pixel in row:
            if(pixel[0] < val):
                pixel[0] = 180 - (val - pixel[0])
            else:
                pixel[0] -= val
    rs, gs, bs = cv2.split(cv2.cvtColor(colorSpace, cv2.COLOR_HSV2RGB))
    return np.uint8((np.uint32(rs) * (255 - np.uint32(bs)) * (255 - np.uint32(gs))) >> 16)


cwd = path.relpath(os.path.dirname(os.path.realpath(__file__)))
#path = path.join(cwd, path.join('images', 'robotview.png'))
trainPath = path.join(cwd, path.join('images', 'pictograph-center.png'))
dataPath = path.join(cwd, path.join('images', 'pictograph-center.png'))

#robotPath = path.join(cwd, 'images', 'robotview.png')

trainImg = cv2.imread(trainPath, 1)
trainImg = cv2.pyrDown(trainImg)
trainImg = cv2.cvtColor(trainImg, cv2.COLOR_BGR2RGB)
trainImgProcessed = process(trainImg)
dataImg = cv2.imread(dataPath, 1)
dataImg = cv2.pyrDown(dataImg)
dataImg = cv2.pyrDown(dataImg)
dataImg = cv2.pyrDown(dataImg)
dataImg = cv2.cvtColor(dataImg, cv2.COLOR_BGR2RGB)
dataImgProcessed = process(dataImg)

orb = cv2.ORB_create()

kpt, dest = orb.detectAndCompute(trainImg, None)
kpd, desd = orb.detectAndCompute(dataImg, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

matches = bf.match(desd, dest)

# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
img3 = None
img3 = cv2.drawMatches(dataImg, kpd, trainImg, kpt, matches[:10], img3, flags=2)
print("here")

plt.imshow(img3)
plt.show()