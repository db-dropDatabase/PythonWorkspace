from enum import Enum, unique

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
    PICTURE_BACKGROUND = "background" # the background of the photo how it normally is

# Perspective
# contains a rotation and translation object, which can be used to determine how the image
# was processed
class Perpective:
    def __init__(self, rotation, translation): #rotation is (X, Y, Z) and translation is the same
        self.rotation = rotation
        self.translation = translation

# Glare
# Not computer generated, just recorded for informational purposes
@unique
class Glare(Enum):
    NONE = "none" # pictogram was digitally edited in
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
    PERFECT = "perfect" # The pictogram was digitally edited in
    # Unfortunatly, we are probably looking at a near dark room due to the sports-like
    # aspect of the competitions later on

# Print Quality
# Again assigned arbitrary values
@unique
class PrintQuality(Enum):
    BAD = "bad" # Faded print
    GOOD = "good" # saturated print
    PERFECT = "perfect" # the pictogram was digitally edited in
    
# Pictogram type
# The thing the neural network wants to get
@unique
class PictogramType(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

# API use example:
# data = GetDataSet(surroundings="bad", type="left")

# img = data.next()
