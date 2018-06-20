import cv2
import numpy as np
import itertools
from ShowImages import show_images
import math
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from mpl_toolkits.axes_grid1 import make_axes_locatable
from skimage import filters

# raise numpy errors (such as divide by zero) so stupid doesn't create more stupid
np.seterr(all="raise")

"""
Simple Hair Removal Algorithm
Based on reverse-engineering http://www.dermweb.com/dull_razor/ through this paper: https://drive.google.com/drive/u/0/folders/1DpVpSvbpg7n3-SoiELW_edkZUYOD0GLy

Uses morphological closing (https://docs.opencv.org/3.4/d9/d61/tutorial_py_morphological_ops.html) to remove low-area features in the image, 
then subtracts the result from the original image to detect areas where features were removed. Otsu's threshold method 
(https://en.wikipedia.org/wiki/Otsu%27s_method) is then appliedto the result of the subtraction, and hysteresis thresholding 
(https://docs.opencv.org/3.1.0/da/d22/tutorial_py_canny.html) is applied to mask hair out of the image. Image is finally removed 
of hair using OpenCV's inpainting algorithms against the mask produced.

Pros:
    - Fast, uses all pre-built C++ bindings from python image processing libraries
    - Good enough, removes the really big hairs, and some of the small ones

Cons:
    - Aggressive, Removes some skin features (such as small dots)
    - Artifacty, can leave behind ridges or shadows (probably can be fixed with tweaking)

This algorithm still needs a little bit of tweaking, so this file uses matplotlib sliders to show the effect of adjusting the low and high thresholds for 
the hysteresis thresholding process.
"""

# Size of kernel for morphological closeing
# larger kernel = larger features detected, may need to be adjusted based on image size
MORPH_CLOSE_SIZE = 7
# Name of image file to load
# All images are assumed "*.jpg"
name = "ISIC_0000032"
# import image as a grayscale image
image = cv2.imread("./Images/Normal/"+name+".jpg", 0)
# downscale resolution by factor of 4 for performance
image = cv2.pyrDown(image)
image = cv2.pyrDown(image)
# morphological closing, removing features with small area
morphrect = cv2.morphologyEx(image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH_CLOSE_SIZE, MORPH_CLOSE_SIZE)))
# subtract closed image from original image, and take the absolute value (casting up to prevent overflow) 
# resulting in large values where there was a dark feature and there isn't one anymore
sub = np.abs(image.astype(np.int16) - morphrect.astype(np.int16)).astype(np.uint8)
# get Otsu's threshold of the subtracted image
# Ostu's method seeks to find the midpoint between two peaks in a histogram. Since we assume that hair and non-hair pixels
# are signifigantly seperated, it's useful here to dynamically determine a threshold.
thresh, img = cv2.threshold(sub, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# NOTE: A good idea here would be to add a threshold for the threshold (if thresh >= num) to detect if hair removal
# for the image is unnesessary, since in testing I have noticed that a lower threshold generally means there is less
# hair present in the image. ENDNOTE
# Process another image when the slider is changed
# The rest of the removal algorithm is located here
def process_image(orgimg, img, lowthresh, highthresh, morphsize):
    # re-apply hysteresis threshold
    img = filters.apply_hysteresis_threshold(sub, lowthresh, highthresh).astype(np.uint8)
    # dilate to expand the area to be inpainted, attempting to cover some
    # shadows/borders left undetected by this algorithm
    img = cv2.dilate(img, cv2.getStructuringElement(cv2.MORPH_RECT, (int(round(morphsize)), int(round(morphsize)))))
    # return the inpainted image
    # NOTE: I haven't messed around with very many inpainting algorithms, I imagine with little bit of research. ENDNOTE
    # would turn up one better suited for skin. ENDNOTE
    return cv2.inpaint(image, img, 10, cv2.INPAINT_NS)
# Before we continue processing, we gotta do some matplotlib stuff
plt.figure()
ax = plt.gca()
implot = ax.imshow(image, cmap="gray")
div = make_axes_locatable(ax)
# make sliders for debug
# low hysteris threshold slider
low = div.append_axes("bottom", size="10%", pad=0.3)
# high hysteris threshold slider
high = div.append_axes("bottom", size="10%", pad=0.3)
# mask dilation kernel size
# mask dilation kernel is used to expand the area to be inpainted, attempting to cover some
# shadows/borders left behind by this algorithm
kern = div.append_axes("bottom", size="10%", pad=0.3)
# setup sliders
low = Slider(low, "Low Thresh", 0, 255, valinit=thresh - 20)
high = Slider(high, "High Thresh", 0, 255, valinit=thresh)
kern = Slider(kern, "Morph Kernel Size", 0, 20, valinit=5)
# on slider change, reprocess and reset the image
onchange = lambda val: implot.set_data(process_image(image, sub, low.val, high.val, int(round(kern.val))))
low.on_changed(onchange)
high.on_changed(onchange)
kern.on_changed(onchange)
# go!
plt.show()

