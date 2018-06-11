import cv2
import numpy as np
import itertools
from ShowImages import show_images
import math
from ComplexHairRemoval import gen_filter_kernel

np.seterr(all="raise")

def run_filter(img, kernel):
    return

# import image as a grayscale image
image = cv2.imread("./Images/Normal/ISIC_0000042.jpg", 0)
image = cv2.pyrDown(image)
image = cv2.pyrDown(image)

morphrect = cv2.morphologyEx(image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)))
morph0 = cv2.morphologyEx(image, cv2.MORPH_CLOSE, gen_filter_kernel(0, math.sqrt(2)))
morph45 = cv2.morphologyEx(image, cv2.MORPH_CLOSE, gen_filter_kernel(45, math.sqrt(2)))
morph90 = cv2.morphologyEx(image, cv2.MORPH_CLOSE, gen_filter_kernel(90, math.sqrt(2)))
morph135 = cv2.morphologyEx(image, cv2.MORPH_CLOSE, gen_filter_kernel(135, math.sqrt(2)))
sub = (image - morphrect)
ret, thresh = cv2.threshold(sub,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

show_images([image, morph0, morph45, morph90, morph135, morphrect, sub, thresh])