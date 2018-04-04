from enum import IntEnum

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
            