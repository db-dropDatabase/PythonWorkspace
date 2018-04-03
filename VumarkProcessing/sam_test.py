from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers.core import Flatten, Dense
from keras.layers.convolutional import MaxPooling2D
import numpy as np
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator


def vgg_16(weights_path=None):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(units=128, activation='relu'))
    model.add(Dense(units=1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    if weights_path:
        model.load_weights(weights_path)
    return model


classifier = vgg_16('class_weightCL.h5')
classifier2 = vgg_16('class_weightCR.h5')
classifier3 = vgg_16('class_weightLR.h5')

#sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True) #the hell is that
#classifier.compile(optimizer=sgd, loss='binary_crossentropy')
#classifier2.compile(optimizer=sgd, loss='binary_crossentropy')
#classifier3.compile(optimizer=sgd, loss='binary_crossentropy')

gen = ImageDataGenerator(rescale=1./255)

def tester(file):
    test_image = image.load_img(str(file), target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = gen.standardize(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = classifier.predict(test_image)
    '''
    if result[0][0] == 1:
        print('left')
    else:
        print('center')
    '''
    result2 = classifier2.predict(test_image)
    '''
    if result2[0][0] == 1:
        print('right')
    else:
        print('center')
    '''
    result3 = classifier3.predict(test_image, batch_size=1)
    '''
    if result3[0][0] == 1:
        print('right')
    else:
        print('left')
    '''
    #if result[0][0] == 1 and result3[0][0] == 0:
        #print('Left')
    #elif result[0][0] == 0 and result2[0][0] == 0:
        #print('Center')
   # elif result2[0][0] == 1 and result3[0][0] == 1:
        #print('Right')
    #else:
        #print('Heck')
    print(result)
    print(result2)
    print(result3)

'''
def dtester():
    while True:
        imp = input('Enter File Name: ')
        try:
            if imp.lower() == 'exit':
                break
            file = imp + '.jpg'
            tester(file)
        except:
            print('Try that again')


dtester()
'''
tester('images/right/0.jpg')