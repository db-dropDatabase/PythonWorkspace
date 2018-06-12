import cv2
import numpy as np
import itertools
from ShowImages import show_images
import math
from ComplexHairRemoval import gen_filter_kernel
from matplotlib import pyplot as plt

np.seterr(all="raise")

def run_filter(img, kernel):
    return

# import image as a grayscale image
image = cv2.imread("./Images/Normal/ISIC_0000042.jpg", 0)
image = cv2.pyrDown(image)
image = cv2.pyrDown(image)

morphrect = cv2.morphologyEx(image, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)))

sub = np.abs(image.astype(np.int16) - morphrect.astype(np.int16)).astype(np.uint8)

thresh, img = cv2.threshold(sub, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

canny = cv2.Canny(sub, 20, 100)

cannyor = cv2.bitwise_or(canny, img)

paint = cv2.inpaint(image, cannyor, 5, cv2.INPAINT_TELEA)

show_images([image, morphrect, sub, img, canny, cannyor, paint])