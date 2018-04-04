from enum import IntEnum
import itertools

# Expanding box blob detection algorithm
# takes a binary image and returns the center of clustered points
# Simple way to clump together corners

class P(IntEnum):
    TOP_LEFT_X = 0
    TOP_LEFT_Y = 1
    BOTTOM_RIGHT_X = 2
    BOTTOM_RIGHT_Y = 3

def _pointInRect(x, y, point):
    return x >= point[P.TOP_LEFT_X] and x <= point[P.BOTTOM_RIGHT_X] and y >= point[P.TOP_LEFT_Y] and y <= point[P.BOTTOM_RIGHT_Y]

def clip(val, minv, maxv):
    if(val < minv):
        return minv
    if(val > maxv):
        return maxv
    return val 

def ExpandingBoxCluster(binImg, maxDist, xSearchDist=0, ySearchDist=0):
    # array of clusters, in form of [[topLeftx, topLefty, bottomRightx, bottomRighty]]
    clustRay = []
    # search every pixel besides the ones already in clusters
    xSearch = binImg.shape[1]
    if xSearchDist != 0:
        xSearch = xSearchDist
    ySearch = binImg.shape[0]
    if ySearchDist != 0:
        ySearch = ySearchDist

    for x in range(maxDist, xSearch - maxDist):
        for y in range(maxDist, ySearch - maxDist):
            # if point is not true or already in a cluster, skip it
            if not binImg[y,x] or any(map(lambda point : _pointInRect(x, y, point), clustRay)):
                continue
            # else get to clustering
            currentRect = [x, y, x, y]
            # python doesn't have a do while
            D = 8
            while 8 == D:
                pointFound = False
                # check the top edge, increasing it if a pixel is found
                if currentRect[P.TOP_LEFT_Y] - maxDist > 0:
                    for tX in range(currentRect[P.TOP_LEFT_X] - maxDist, currentRect[P.BOTTOM_RIGHT_X] + maxDist + 1):
                        if binImg[currentRect[P.TOP_LEFT_Y] - maxDist, tX]:
                            currentRect[P.TOP_LEFT_Y] -= maxDist
                            pointFound = True
                            break
                # bottom
                if currentRect[P.BOTTOM_RIGHT_Y] + maxDist + 1 < binImg.shape[0]:
                    for tX in range(currentRect[P.TOP_LEFT_X] - maxDist, currentRect[P.BOTTOM_RIGHT_X] + maxDist + 1):
                        if binImg[currentRect[P.BOTTOM_RIGHT_Y] + maxDist, tX]:
                            currentRect[P.BOTTOM_RIGHT_Y] += maxDist
                            pointFound = True
                            break
                # left
                if currentRect[P.TOP_LEFT_X] - maxDist > 0:
                    for tY in range(currentRect[P.TOP_LEFT_Y] - maxDist, currentRect[P.BOTTOM_RIGHT_Y] + maxDist + 1):
                        if binImg[tY, currentRect[P.TOP_LEFT_X] - maxDist]:
                            currentRect[P.TOP_LEFT_X] -= maxDist
                            pointFound = True
                            break
                # right
                if currentRect[P.BOTTOM_RIGHT_X] + maxDist + 1 < binImg.shape[1]:
                    for tY in range(currentRect[P.TOP_LEFT_Y] - maxDist, currentRect[P.BOTTOM_RIGHT_Y] + maxDist + 1):
                        if binImg[tY, currentRect[P.BOTTOM_RIGHT_X] + maxDist]:
                            currentRect[P.BOTTOM_RIGHT_X] += maxDist
                            pointFound = True
                            break
                # if we didn't find any points searching around, finish cluster
                if not pointFound:
                    break
            clustRay.append(currentRect)
    return clustRay

# Sort points by visible and nonvisible from a center point, with on pixels acting as walls
# returns [[visible], [nonvisible]]
def RayCastClassifier(binImg, blobs, centerX, centerY):
    ret = ([], [])
    for blob in blobs:
        # reduce blob point duplicates
        points = []
        for i in range(2):
            if not any(map(lambda p: p == (blob[i], blob[i+1]), points)):
                points.append((blob[i], blob[i+1]))
        # ray cast test every point left
        # functional programming ftw
        if any(map(lambda point: 
            any(map(lambda linePoint: 
                binImg[linePoint[1], linePoint[0]], 
            get_line((centerX, centerY), (point[0], point[1])))), 
        points)):
            ret[1].append(blob)
        else:
            ret[0].append(blob)
    return ret


def get_line(start, end):
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    # Swap start and end points if necessary and store swap state
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
    # Iterate over bounding box generating points between start and end
    y = y1
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        yield coord
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx