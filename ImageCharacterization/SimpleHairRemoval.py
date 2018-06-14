import cv2
import numpy as np
import itertools
from ShowImages import show_images
import math
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from mpl_toolkits.axes_grid1 import make_axes_locatable
from skimage import filters

np.seterr(all="raise")

def process_image(orgimg, img, lowthresh, highthresh, morphsize):
    img = filters.apply_hysteresis_threshold(sub, lowthresh, highthresh).astype(np.uint8)
    img = cv2.dilate(img, cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)))
    return cv2.inpaint(image, img, morphsize, cv2.INPAINT_NS)

MIN_THRESH = 30.0 # greater than or equal to for additional hair removal
SECOND_MORPH = 5
QUESTIONABLE = "ISIC_0000032"
name = "ISIC_0000032"

# import image as a grayscale image
image = cv2.imread("./Images/Normal/"+name+".jpg", 0)
image = cv2.pyrDown(image)
image = cv2.pyrDown(image)

morphrect = cv2.morphologyEx(image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)))

sub = np.abs(image.astype(np.int16) - morphrect.astype(np.int16)).astype(np.uint8)

thresh, img = cv2.threshold(sub, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

print(thresh)

hyst = filters.apply_hysteresis_threshold(sub, thresh - 20, thresh)

plt.figure()
ax = plt.gca()
implot = ax.imshow(image, cmap="gray")
div = make_axes_locatable(ax)
low = div.append_axes("bottom", size="10%", pad=0.3)
high = div.append_axes("bottom", size="10%", pad=0.3)
kern = div.append_axes("bottom", size="10%", pad=0.3)
low = Slider(low, "Low Thresh", 0, 255, valinit=thresh - 20)
high = Slider(high, "High Thresh", 0, 255, valinit=thresh)
kern = Slider(kern, "Morph Kernel Size", 0, 20, valinit=5)
onchange = lambda val: implot.set_data(process_image(image, sub, low.val, high.val, int(round(kern.val))))
low.on_changed(onchange)
high.on_changed(onchange)
kern.on_changed(onchange)

#show_images([image, morphrect, sub, img, hyst])

plt.show()

