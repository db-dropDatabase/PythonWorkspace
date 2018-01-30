from enum import Enum, unique
import itertools
import random

# Dataset Generation API
# Surroundings (background behind picture)
# Perpsective (rotation and translation)
# Reflection/Glare
# Lighting conditions
# Print fading
# Resolution 330x270
# Type: (left, right, center)

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
    def __init__(self, imgPath, surroundings, perspective, glare, lighting, printQual, pictogramType, blur, balls):
        self.imgPath = imgPath
        self.surroundings = surroundings
        self.perspective = perspective
        self.glare = glare
        self.lighting = lighting
        self.printQual = printQual
        self.pictogramType = pictogramType
        self.blur = blur
        self.balls = balls

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

def DataIterator(surroundings=list(Surroundings), 
                 glare=list(Glare),    
                 lighting=list(Lighting), 
                 printQuality=list(PrintQuality), 
                 pictogramType=list(PictogramType), 
                 blur=list(Blur), 
                 balls=list(Balls),
                 randomizePerspective=False):
    # check every argument if value or array
    combo = [pictogramType, surroundings, glare, lighting, printQuality, blur, balls]
    combo = map(wrapList, combo)
    
    # generate every permutation
    perm = list(itertools.product(*combo))
    # shuffle it
    random.shuffle(perm)
    # iterate through it, returning a new object for each next() call
    

DataIterator()