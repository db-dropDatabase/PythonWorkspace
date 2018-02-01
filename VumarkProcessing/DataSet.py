from enum import Enum, unique
import itertools
import random
import json
import cv2

# Dataset Generation API
# Surroundings (background behind picture)
# Perpsective (rotation and translation)
# Reflection/Glare
# Lighting conditions
# Print fading
# Resolution 330x270
# Type: (left, right, center)

PATH = 'C:\\Users\\Noah\\Documents\\code\\DataSet'

# Surroundings
# e.g. everywhere the pictogram isn't
@unique
class Surroundings(Enum):
    GENERATED_NOISE = "noise" # noise created by randomizing each pixel
    BLACK = "black" # a solid black
    MISMATCH_BACKGROUND = "misback"
    PICTURE_BACKGROUND = "background" # the background of the photo how it normally is

# Perspective
# contains a rotation and translation object, which can be used to determine how the image
# was processed
class Perspective:
    def __init__(self, rotation, translation): #rotation is (X, Y, Z) and translation is the same
        self.rotation = rotation
        self.translation = translation
    
    # Function to correct the image according to the perspective information
    def getCorrectedImage(self, img):
        #TODO: this function
        return False

# Glare
# Not computer generated, just recorded for informational purposes
@unique
class Glare(Enum):
    PAPER = "paper" # only catches ambient light reflecting off of the paper
    PLASTIC_SLEVE = "plastic" # catches light reflecting off of the plastic sleve
    PLEXIGLASS_COVER = "plexi" # catches light reflecting off of a sctratched plexiglass cover
    FLASHLIGHT_PLEXIGLASS = "flashlight" # flashlight is reflected off of the same plexiglass to intentionally obscure camera 
    # the above is probably closest to real world situations
    # the rest are provided for additional training

# Lighting
# The amount of surrounding lights, arbitrarily assigned values
@unique
class Lighting(Enum):
    NONE = "none" # A dark room
    POOR = "poor" # A not very well lit room
    GOOD = "good" # The best lighting availible given the equipment I have
    # Unfortunatly, we are probably looking at a near dark room due to the sports-like
    # aspect of the competitions later on

# Print Quality
# Again assigned arbitrary values
@unique
class PrintQuality(Enum):
    GOOD = "good" # saturated print
    BAD = "bad" # Faded print

# Pictogram type
# The thing the neural network wants to get
@unique
class PictogramType(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

# Blur, as in we shook the camera on accident
@unique
class Blur(Enum):
    NONE = "none"
    BLURRED = "blur"

# Ball present in image
# Will be present in the right corner of the pictogram if at all
@unique
class Balls(Enum):
    NONE = "none"
    BLUE = "blue"
    RED = "red"

# Class to represent the pictograms location within the image
class PictogramLocation:
    def __init__(self, points): # points are ((x, y), (x, y), (x, y), (x, y)) in pixels of corners 
    # in order of ((bottom left, top left, top right, bottom right)) 
        self.points = points
    # returns just the pictogram image cut out of the rest of the image
    def getLocalizedPictogram(self, img):
        #TODO: this function
        return False


class Pictogram:
    # each bit of data that can be assigned to a given pictogram picture
    # first the path of the image, then please use the above enums
    def __init__(self, img, surroundings, perspective, glare, lighting, printQual, pictogramType, blur, balls, location):
        self.img = img
        self.surroundings = surroundings
        self.perspective = perspective
        self.glare = glare
        self.lighting = lighting
        self.printQual = printQual
        self.pictogramType = pictogramType
        self.blur = blur
        self.balls = balls
        self.picLoc = location

    # applies the image transforms necessary and returns the pictogram
    def getImage(self):
        #TODO this function
        return False

# API use example:
# data = GetDataSet(surroundings="bad", type="left")

# img = data.next()

def wrapList(item):
    if hasattr(item, "__len__"):
        return item
    else:
        return [item]

def stringListToCoords(str):
    ray = json.loads('[' + str + ']')
    tempRay = [0, 0, 0, 0]
    # map flat string to coordinate arrays
    if len(ray) > 0:
        for i in range(0, 4):
            tempRay[i] = (ray[i * 2], ray[i * 2 + 1])
        # sort by X coordinate
        tempRay.sort(key=lambda coord: coord[0])
        # if Y of point 0 is greater than Y of point 1 and the opposite is true of the Y's of the next two points, switch em
        # also vice versa
        if (tempRay[0][1] > tempRay[1][1] and tempRay[2][1] > tempRay[3][1]) or (tempRay[0][1] < tempRay[1][1] and tempRay[2][1] < tempRay[3][1]):
            tempRay = (tempRay[0], tempRay[1], tempRay[3], tempRay[2])
        # switch points so origin is always a bottom left
        if tempRay[0][1] < tempRay[1][1]:
            return (tempRay[1], tempRay[0], tempRay[3], tempRay[2])
        else:
            return tempRay
    else:
        return None

def filterPictures(objs, critRay):
    def isMatch(pic):
        return  (pic['type'] == critRay[0].value 
                and pic['glare'] == critRay[2].value
                and pic['light'] == critRay[3].value
                and pic['print'] == critRay[4].value
                and pic['blur'] == critRay[4].value
                and pic['balls'] == critRay[5].value)

    return filter(isMatch, objs)

def DataIterator(dataObject, # the parsed JSON from the dataset
                 loops, # the # of times to loop through every combination of factor
                 # using different images this time
                 surroundings=list(Surroundings), 
                 glare=list(Glare),    
                 lighting=list(Lighting), 
                 printQuality=list(PrintQuality), 
                 pictogramType=list(PictogramType), 
                 blur=list(Blur), 
                 balls=list(Balls),
                 randomizePerspective=False): # not currently implemented
        
    # check every argument if value or array
    combo = [pictogramType, surroundings, glare, lighting, printQuality, blur, balls]
    combo = map(wrapList, combo)
    
    # generate every permutation
    perm = list(itertools.product(*combo))
    # shuffle it
    random.shuffle(perm)
    # iterate through it, returning a new object for each next() call
    for i in range(loops):
        for item in perm:
            # if the surroundings are normal, find a picture that matches all the criteria
            if item[1] == Surroundings.PICTURE_BACKGROUND:
                ray = filterPictures(dataObject, item)
                if len(ray) == 0:
                    print("skipping: ")
                    print(item)
                else:
                    picItem = random.choice(ray)
                    # remove the image from the data so we don't pick it again
                    dataObject[next((i for i in range(len(dataObject)) if dataObject[i]['id'] == picItem['id']))]['match'] = True
                    # return the pictogram object
                    yield Pictogram(
                        cv2.imread(os.path.join(PATH, picItem['type'], picItem['name'])),
                        Surroundings.PICTURE_BACKGROUND,
                        None,
                        Glare(picItem['glare']),
                        Lighting(picItem['lighting']),
                        PrintQuality(picItem['print']),
                        PictogramType(picItem['type']),
                        Blur(picItem['blur']),
                        Balls(picItem['balls']),
                        stringListToCoords(picItem['picto'])
                    )
            else if item[1] == Surroundings.MISMATCH_BACKGROUND:
                



DataIterator(None, 2)