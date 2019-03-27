from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Conv1D
from keras.layers import Conv2D
from keras.layers import MaxPooling1D
from keras.layers import MaxPooling2D
from keras.layers.core import Reshape
from keras.layers import Flatten
from keras import optimizers as opt


def createModel():
    model = Sequential()
    #(1,1,15000)    每一个数据是一个1维数据
    model.add(Conv1D(filters=20, kernel_size = 200, strides= 1,padding = 'valid', input_shape=(15000,1),activation='relu'))
    print(model.input_shape)
    print("C1：",end="")
    print(model.output_shape)
    #15000-199(移动199次
    #(20,1,14801)   每一个数据是一个1维数据，只是一个epoch上取了20个数据
    model.add(MaxPooling1D(pool_size=20, strides=10, padding='valid'))
    print("P1：",end="")
    print(model.output_shape)
    #(20,1,1479)（数据变为原来的1/10
    #stacking, h201d变为h1 的20维数据
    #stacking layer
    print("Stacking layer：",end="")
    model.add(Reshape([20,-1,1]))
    print(model.output_shape)

    model.add(Conv2D(filters=400, kernel_size = (20,30), strides= 1,padding = 'valid',activation='relu',data_format='channels_last'))
    print("C2：",end="")
    print(model.output_shape)
    model.add(MaxPooling2D(pool_size=(1,10), strides=2, padding='valid',data_format='channels_last'))
    print("P2：",end="")
    print(model.output_shape)

    model.add(Flatten(data_format='channels_last'))
    print(model.output_shape)

    model.add(Dense(500,activation='relu'))
    print("M1：",end="")
    print(model.output_shape)
    model.add(Dense(500,activation='relu'))
    print("M2：",end="")
    print(model.output_shape)

    model.add(Dense(5,activation='softmax'))
    print(model.output_shape)
    model.compile(optimizer=opt.SGD(lr = 0.00005), loss='categorical_crossentropy', metrics=['accuracy'])
    return model