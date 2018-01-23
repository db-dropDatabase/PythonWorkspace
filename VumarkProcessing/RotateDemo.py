import cv2
import matplotlib
import numpy as np
import os
from os import path
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from mpl_toolkits.axes_grid1 import make_axes_locatable
from VertSlider import VertSlider
from RotateImage import rotateImage

path = path.relpath(path.join('images', 'relicDemo.jpg'))

img = cv2.imread(path, 0)

IMG_SHAPE = img.shape
IMG_WIDTH = IMG_SHAPE[1]
IMG_HEIGHT = IMG_SHAPE[0]

# Start Main
# Create slider for the image rotating
plt.figure()
ax = plt.gca()

imgGood = rotateImage(img, 0, 0, 0, 0, 0, 300., 300.)
imPlot = ax.imshow(imgGood, cmap = 'gray', interpolation = 'bicubic')

div = make_axes_locatable(ax)
alpha = div.append_axes("bottom", size="10%", pad=0.3)
beta = div.append_axes("right", size="5%", pad=0.3)
gamma = div.append_axes("top", size="10%", pad=0.3)

sBeta = VertSlider(beta, "X Axis", 0, 180, valinit=0)
sAlpha = Slider(alpha, "Y Axis", 0, 180, valinit=0)
sGamma = Slider(gamma, "Z Axis", 0, 180, valinit=0)

def update(val):
    imPlot.set_data(rotateImage(img, sBeta.val, sAlpha.val, sGamma.val, 0, 0, 800., 800.))

sAlpha.on_changed(update)
sBeta.on_changed(update)
sGamma.on_changed(update)

plt.show()
