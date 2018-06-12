import cv2
import numpy as np
import itertools
from ShowImages import show_images
import math

np.seterr(all="raise")

# Based on this paper: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.1006.4419&rep=rep1&type=pdf
# Generate gaussianish curvilinear filter based on a direction and std. dev
def gen_filter_kernel(angleDirection, stdDev):
    """Generate gaussianish curvilinear filter based on a direction and std. dev
    Based on this paper: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.1006.4419&rep=rep1&type=pdf

    Args:
        angleDirection (float): Direction to filter (since filter is linear) in degrees
        stdDev: Size of filter to use

    Returns:
        numpy.array: The kernel to be filtered with
    """
    # Generate unit vector based on direction
    v = (np.cos(np.radians(angleDirection)), np.sin(np.radians(angleDirection)))
    # calculate size of kernel
    size = math.floor(6*stdDev)
    # calculate a centerPoint
    centerPoint = math.ceil(size/2) - 1 
    # ensure an integer center
    if size % 2 == 0:
        size -= 1
    # Create kernel based on size of stdDev
    kernel = np.zeros((size, size))
    # for every value in the kernel
    for x, y in itertools.product(range(size), repeat=2):
        # dot productof point minus center and unit vector
        dp2 = (x - centerPoint)*v[0] + (y - centerPoint)*v[1]
        # gaussian stuff
        # opencv is row major
        kernel[y, x] = np.exp(-np.square(dp2)/(2*np.square(stdDev)))
    # normalize kernel
    kernel -= np.amin(kernel)
    kernel /= np.amax(kernel)
    kernel *= 255
    kernel = kernel.astype(np.uint8)
    # return generated kernel
    return kernel

def convolve_test(img, kernels):
    """ Custom convolve image based on a given array of filter kernels
    Based on math used in http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.1006.4419&rep=rep1&type=pdf

    Args:
        img (numpy.array): CV_8U greyscale image
        kernels (iterable(numpy.array)): Array of CV_64F filtering kernels of the same square shape.
    
    Returns:
        numpy.array: shape of img, the maximum convolved value for each pixel
    """
    # create return object
    outImg = np.zeros(img.shape)
    # get window +- from kernel size
    windowDelta = math.floor(kernels[0].shape[0] / 2)
    # for every pixel in the image
    for x,y in itertools.product(range(windowDelta, img.shape[1] - windowDelta), range(windowDelta, img.shape[0] - windowDelta)):
        # slice window from image
        window = img[y - windowDelta:y + windowDelta + 1, x - windowDelta:x + windowDelta + 1].copy()
            # get the output value for every kernel
        outputs = list(map(lambda kernel: run_filter(window, kernel), kernels))
        # and the return the maximum
        outImg[y, x] = np.amax(outputs)
    return outImg

def run_filter(window, kernel):
    """ Run custom convulution given a kernel and a window of matching size

    Args:
        window (numpy.array): grayscale image segment
        kernel (numpy.array): filtering kernel to apply
    
    Returns:
        numpy.float64: The convulution result
    """
    # normalize window to 0-1 values
    window -= np.amin(window)
    windowMax = np.amax(window)
    # if image is completly similair ignore it
    if windowMax == 0:
        return 0
    window = window / windowMax
    # get the sum of the product of the filter and the image
    productSum = np.sum(window * kernel)
    # get the sum of the square of every pixel of kernel and image
    windowSum = np.sum(np.square(window))
    kernelSum = np.sum(np.square(kernel))
    # return the final score
    return np.square(productSum)/(windowSum*kernelSum)

"""
# import image as a grayscale image
image = cv2.imread("./Images/Normal/ISIC_0000042.jpg", 0)
image = cv2.pyrDown(image)
image = cv2.pyrDown(image)
image = cv2.pyrDown(image)
image = cv2.pyrDown(image)
# invert
image = 255 - image

# display 
show_images([image] + list(map(lambda stuff: convolve_test(image, [gen_filter_kernel(stuff[0], stuff[1])]), itertools.product(range(0, 190, 30), [2*math.sqrt(2)]))))

"""