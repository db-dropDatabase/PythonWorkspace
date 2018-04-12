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
def RayCastClassifier(binImg, blobs, centerX, centerY, debugImage=(), startIter=0):
    ret = ([], [])
    for blob in blobs:
        # reduce blob point duplicates
        points = []
        for i in range(2):
            if not any(map(lambda p: p == (blob[i*2], blob[i*2+1]), points)):
                points.append((blob[i*2], blob[i*2+1]))
        # ray cast test every point left
        # functional programming ftw
        if any(map(lambda point: 
            any(map(lambda linePoint: 
                binImg[linePoint[1], linePoint[0]], 
            get_line((centerX, centerY), (point[0], point[1]), startIter=startIter))), 
        points)):
            ret[1].append(blob)
        else:
            ret[0].append(blob)
        if len(debugImage) > 0:
            for point in points:
                for linePoint in get_line((centerX, centerY), (point[0], point[1])):
                    debugImage[linePoint[1], linePoint[0]] = (0, 255, 0)
    return ret


def get_line(start, end, startIter=0):
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
    # start with one iteration
    for i in range(startIter):
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
    for x in range(x1 + startIter, x2 - startIter):
        coord = (y, x) if is_steep else (x, y)
        yield coord
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

# taken from https://stackoverflow.com/questions/6989100/sort-points-in-clockwise-order
def ClockwisePointSort(center, points):
    def clockWiseCompare(a, b): # returns 1 if greater, 0 if same, -1 if less
        nonlocal center
        if a == b:
            return 0
        if a[0] - center[0] >= 0 and b[0] - center[0] < 0:
            return -1
        if a[0] - center[0] < 0 and b[0] - center[0] >= 0:
            return 1
        if a[0] - center[0] == 0 and b[0] - center[0] == 0:
            if a[1] - center[1] >= 0 or b[1] - center[1] >= 0:
                if a.y > b.y:
                    return -1
                else:
                    return 1
            if b.y > a.y:
                return -1
            else:
                return 1
        # compute the cross product of vectors (center -> a) x (center -> b)
        det = (a[0] - center[0]) * (b[1] - center[1]) - (b[0] - center[0]) * (a[1] - center[1])
        if det < 0:
            return -1
        if det > 0:
            return 1
        # points a and b are on the same line from the center
        # check which point is closer to the center
        d1 = (a[0] - center[0]) * (a[0] - center[0]) + (a[1] - center[1]) * (a[1] - center[1])
        d2 = (b[0] - center[0]) * (b[0] - center[0]) + (b[1] - center[1]) * (b[1] - center[1])
        if d1 > d2:
            return -1
        else:
            return 1
    # sort points using clockwisecompare
    return sorted(points, key=cmp_to_key(clockWiseCompare))

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K
