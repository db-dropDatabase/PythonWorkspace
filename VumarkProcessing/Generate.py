import cv2
import matplotlib
import numpy as np
import os
from os import path
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math
from math import sin
from math import cos
from VertSlider import VertSlider

PADDING_X = 100
PADDING_Y = 100

path = path.relpath(path.join('folder', 'relicDemo.jpg'))

img = cv2.imread(path, 0)

IMG_SHAPE = img.shape
IMG_WIDTH = IMG_SHAPE[1]
IMG_HEIGHT = IMG_SHAPE[0]

# The parameters are:
# input: the image that you want rotated.
# output: the Mat object to put the resulting file in.
# alpha: the rotation around the x axis
# beta: the rotation around the y axis
# gamma: the rotation around the z axis (basically a 2D rotation)
# dx: translation along the x axis
# dy: translation along the y axis
# dz: translation along the z axis (distance to the image)
# f: focal distance (distance between camera and image, a smaller number exaggerates the effect)
# code stolen from: http://jepsonsblog.blogspot.com/2012/11/rotation-in-3d-using-opencvs.html
# 90 degrees is normal position

def rotateImage(input, alpha, beta, gamma, dx, dy, dz, f):
    # radians
    alpha = alpha*math.pi/180.
    beta = beta*math.pi/180.
    gamma = gamma*math.pi/180.
    #shift dx and dy so the image is centered
    dx += PADDING_X
    dy += PADDING_Y
    # get width and height for ease of use in matrices
    w = np.float64(input.shape[1])
    h = np.float64(input.shape[0])
    # Projection 2D -> 3D matrix
    A1 = np.matrix((
            (1, 0, -w/2),
            (0, 1, -h/2),
            (0, 0,    0),
            (0, 0,    1)
        ), dtype=np.float64)
    # Rotation matrices around the X, Y, and Z axis
    RX = np.matrix((
            (1,          0,           0, 0),
            (0, cos(alpha), -sin(alpha), 0),
            (0, sin(alpha),  cos(alpha), 0),
            (0,          0,           0, 1)
        ), dtype=np.float64)
    RY = np.matrix((
            (cos(beta), 0, -sin(beta), 0),
            (0, 1,          0, 0),
            (sin(beta), 0,  cos(beta), 0),
            (0, 0,          0, 1)
        ), dtype=np.float64)
    RZ = np.matrix((
            (cos(gamma), -sin(gamma), 0, 0),
            (sin(gamma),  cos(gamma), 0, 0),
            (0,          0,           1, 0),
            (0,          0,           0, 1)
        ), dtype=np.float64)
    # Composed rotation matrix with (RX, RY, RZ)
    R = RX * RY * RZ
    # Translation matrix
    T = np.matrix((
            (1, 0, 0, dx),
            (0, 1, 0, dy),
            (0, 0, 1, dz),
            (0, 0, 0, 1)
        ), dtype=np.float64)
    # 3D -> 2D matrix
    A2 = np.matrix((
            (f, 0, w/2, 0),
            (0, f, h/2, 0),
            (0, 0,   1, 0),
        ), dtype=np.float64)
    # Final transformation matrix
    trans = A2 * (T * (R * A1))
    # Apply matrix transformation
    return cv2.warpPerspective(input, trans, (input.shape[1] + PADDING_X*2, input.shape[0] + PADDING_Y*2), cv2.INTER_LANCZOS4)

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
