import cv2
import matplotlib
import numpy as np
import os
from os import path
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from mpl_toolkits.axes_grid1 import make_axes_locatable

def process(hsvimg, degrees):
    """"
    degrees = int(round(degrees))
    for row in hsvimg:
        for pixel in row:
            if(pixel[0] < degrees):
                pixel[0] = 180 - (degrees - pixel[0])
            else:
                pixel[0] -= degrees
    """
    h,s,v = cv2.split(hsvimg)
    r,g,b = cv2.split(cv2.cvtColor(hsvimg, cv2.COLOR_HSV2RGB))
    #return np.uint8((np.uint32(r) * (255 - np.uint32(b)) * (255 - np.uint32(g))) >> 16)
    return np.uint8((np.uint16(r) * (np.uint16(s))) >> 8)


cwd = path.relpath(os.path.dirname(os.path.realpath(__file__)))
path = path.join(cwd, path.join('images', 'robotview.png'))
#path = path.join(cwd, path.join('images', '81.jpg'))
#robotPath = path.join(cwd, 'images', 'robotview.png')

img = cv2.imread(path, 1)
#img = cv2.pyrDown(img)
#img = cv2.pyrDown(img)
img = cv2.pyrDown(img)
img = cv2.pyrDown(img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

IMG_SHAPE = img.shape
IMG_WIDTH = IMG_SHAPE[1]
IMG_HEIGHT = IMG_SHAPE[0]

#convert to HSV
img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

# Start Main
# Create slider for the image rotating
plt.figure()
ax = plt.gca()

implot = ax.imshow(process(img, 0), cmap="gray")

div = make_axes_locatable(ax)
orange = div.append_axes("bottom", size="10%", pad=0.3)
orange = Slider(orange, "Hue Shift (x2)", -180, 180, valinit=0)
orange.on_changed(lambda val: implot.set_data(process(img.copy(), orange.val)))

plt.show()
