import DataSet
import os
import cv2
import pickle
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from mpl_toolkits.axes_grid1 import make_axes_locatable

def makeRadioAxes(div, where, size, pad, enum):
    temp = div.append_axes(where, size=size, pad=pad)
    temp.set_title(enum.__name__)
    return RadioButtons(temp, [i.value for i in enum])

BUTTON_ENUMS = (DataSet.Glare, DataSet.Lighting, DataSet.PrintQuality, DataSet.Blur, DataSet.Balls)
buttonVars = [list(i)[0] for i in BUTTON_ENUMS]
pictoRay = []

# for every image in a folder, ask the user to specify some qualities about the image
# catigoizing the data for our neural net

cwd = os.path.relpath(os.path.dirname(os.path.realpath(__file__)))
path = os.path.join(cwd, os.path.join('images', 'sampledata.jpg'))
imgFolderPath = "C:/Users/Noah/Documents/code/DataSet/right"
index = 0
fnames = tuple(filter(lambda f : f.endswith(".jpg"), [os.fsdecode(f) for f in os.listdir(imgFolderPath)]))

# Load sample image
img = cv2.imread(os.path.join(imgFolderPath, fnames[index]), 1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Build matplotlib display
plt.figure()
ax = plt.gca()

imPlot = ax.imshow(img)

div = make_axes_locatable(ax)
# buttons
buttons = [makeRadioAxes(div, "right", "20%", 0.1, enum) for enum in BUTTON_ENUMS]
# callbacks
# sigh
def callBack0(ev):
    buttonVars[0] = ev
buttons[0].on_clicked(callBack0)
def callBack1(ev):
    buttonVars[1] = ev
buttons[1].on_clicked(callBack1)
def callBack2(ev):
    buttonVars[2] = ev
buttons[2].on_clicked(callBack2)
def callBack3(ev):
    buttonVars[3] = ev
buttons[3].on_clicked(callBack3)
def callBack4(ev):
    buttonVars[4] = ev
buttons[4].on_clicked(callBack4)

nextBut = div.append_axes("right", size="20%", pad=0.1)
nextBut = Button(nextBut, "Next")
def next(ev):
    global index
    pictoRay.append(DataSet.Pictogram(path, None, None, buttonVars[0], buttonVars[1], buttonVars[2], DataSet.PictogramType.RIGHT, buttonVars[3], buttonVars[4]))
    index += 1
    if index >= len(fnames):
        file = open(os.path.join(imgFolderPath, 'pickleFile'), 'w')
        pickle.dump(pictoRay, file, protocol=pickle.HIGHEST_PROTOCOL)
        exit(status=0, message="Finished succesfully")
    img = cv2.imread(os.path.join(imgFolderPath, fnames[index]), 1)
    imPlot.set_data(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    print("next")
nextBut.on_clicked(next)

plt.show()

print(pictoRay)

file = open(os.path.join(imgFolderPath, 'pickleFile'), 'wb')
pickle.dump(pictoRay, file, protocol=pickle.HIGHEST_PROTOCOL)