import cv2
import matplotlib
import numpy as np
import os
from os import path
from matplotlib import pyplot as plt
from ShowImagesMatPlot import show_images

cwd = path.relpath(os.path.dirname(os.path.realpath(__file__)))
path = path.join(cwd, path.join('images', 'robotview.png'))

img = cv2.imread(path, 1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

pyr1 = cv2.pyrDown(img)
pyr2 = cv2.pyrDown(pyr1)
pyr3 = cv2.pyrDown(pyr2)

show_images((pyr1, pyr2, pyr3))

