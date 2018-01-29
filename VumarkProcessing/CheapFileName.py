import DataSet
import os
import pickle

SET = "C:/Users/Noah/Documents/code/DataSet/"
FOLDER = "left"


cwd = os.path.relpath(os.path.dirname(os.path.realpath(__file__)))
path = os.path.join(cwd, os.path.join('images', 'sampledata.jpg'))
imgFolderPath = SET + FOLDER
fnames = tuple(filter(lambda f : f.endswith(".jpg"), [os.fsdecode(f) for f in os.listdir(imgFolderPath)]))
for i in range(len(fnames)):
    os.rename(os.path.join(imgFolderPath, fnames[i]), os.path.join(imgFolderPath, str(i) + FOLDER + '.jpg'))