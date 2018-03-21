import cv2
import math
from math import sin
from math import cos
import numpy as np

PADDING_X = 100
PADDING_Y = 100

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
