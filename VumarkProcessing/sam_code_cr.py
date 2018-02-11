from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
import DataSet
from DataSet import PictogramType
import json

# get the JSON and parse it
def mapDict(item):
    str = '[' + item['picto'] + ']'
    ray = json.loads(str)
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
            item['picto'] = (tempRay[1], tempRay[0], tempRay[3], tempRay[2])
        else:
            item['picto'] = tempRay
    else:
        item['picto'] = None
    return item

def nn(testIter, trainIter, name):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(units=128, activation='relu'))
    model.add(Dense(units=1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    
    model.fit_generator(trainIter,
                        steps_per_epoch=300,
                        epochs=3,
                        validation_data=testIter,
                        validation_steps=20)
    model.save_weights(name + '.h5')
    return model

with open("mostOfThem.json", 'r') as f:
    data = json.load(f)

data = tuple(map(mapDict, filter(lambda item: PictogramType.has_value(item['type']), data)))

train_datagen = ImageDataGenerator(rescale=1./255,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)

'''
nn( DataSet.DataIterator(data, 
                32, 
                None, 
                test_datagen,
                PictogramType.LEFT, 
                pictogramType=(PictogramType.CENTER, PictogramType.LEFT),
                surroundings=DataSet.Surroundings.PICTURE_BACKGROUND), 
    DataSet.DataIterator(data, 
                32, 
                None, 
                train_datagen,
                PictogramType.LEFT, 
                pictogramType=(PictogramType.CENTER, PictogramType.LEFT)),
    'class_weightCL')
'''
nn( DataSet.DataIterator(data, 
                32, 
                None, 
                test_datagen,
                PictogramType.RIGHT, 
                pictogramType=(PictogramType.CENTER, PictogramType.RIGHT),
                surroundings=DataSet.Surroundings.PICTURE_BACKGROUND), 
    DataSet.DataIterator(data, 
                32, 
                None, 
                train_datagen,
                PictogramType.RIGHT, 
                pictogramType=(PictogramType.CENTER, PictogramType.RIGHT)),
    'class_weightCR')
'''
nn( DataSet.DataIterator(data, 
                32, 
                None, 
                test_datagen,
                PictogramType.RIGHT, 
                pictogramType=(PictogramType.LEFT, PictogramType.RIGHT),
                surroundings=DataSet.Surroundings.PICTURE_BACKGROUND), 
    DataSet.DataIterator(data, 
                32, 
                None, 
                train_datagen,
                PictogramType.RIGHT, 
                pictogramType=(PictogramType.LEFT, PictogramType.RIGHT)),
    'class_weightLR')
    '''