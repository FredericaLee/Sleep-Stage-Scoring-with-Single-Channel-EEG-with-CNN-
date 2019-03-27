import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# import os
# os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"]="0,1"

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Conv1D
from keras.layers import Conv2D
from keras.layers import MaxPooling1D
from keras.layers import MaxPooling2D
from keras.layers.core import Reshape
from keras.layers import Flatten
from keras import optimizers as opt
import data_process
import numpy as np
from keras import utils
import copy


#############################准备数据##############################
ba =3
Bsizes = [290]
# countr, count1, count2, count3,countw,start,end,listlable = data_process.getLabel()
# re = data_process.getV(start,end)
# boxs = data_process.Box(countr,count1,count2,count3,countw)
# data,lable =data_process.BoxV(boxs,re,listlable)
# x_train = np.array(data[1] + data[2] + data[3] + data[4])
# y_train = np.array(lable[1] + lable[2] + lable[3] + lable[4])
# x_test = np.array(data[0])
# y_test = np.array(lable[0])
# # x_train = [data[0][0],data[0][1]]
# # y_train = [lable[0][0],lable[0][1]]
# # x_test = [data[0][0]]
# # y_test = [lable[0][0]]
#
# # x_train = re
# # y_train = listlable
# x_train = np.expand_dims(x_train, axis=2)
# x_test = np.expand_dims(x_test, axis=2)
#
# y_train = utils.to_categorical(y_train)
# y_test = utils.to_categorical(y_test)
#
# np.save("x_train.npy",x_train)
# np.save("y_train.npy",y_train)
# np.save("x_test.npy",x_test)
# np.save("y_test.npy",y_test)

# x_train = np.load("x_train.npy")
# x_test = np.load("x_test.npy")
# y_train = np.load("y_train.npy")
# y_test = np.load("y_test.npy")
# print(x_train.shape)
print("数据准备完成")
#############################定义网络##############################
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
    return model

#############################训练网络##############################
fold = 20   #20折交叉验证
acc = 0
for i in range(0,1): #分集
    model    =  createModel()
    print("模型装载成功")

    for j in range(0,1):
        # xi = 0
        # yi = 0
        print("开始训练：")
        model.fit(x_train,y_train,epochs = 10,batch_size=290)
        score = model.evaluate(x_test,y_test)
        acc = acc +score[1]
        print(str(i)+": "+str(score[1]))
    print("Acc: "+str(acc/1))


# print(len(x_train))
# print(x_train[0])
# print(len(x_train[0]))
# print(len(y_train))
# print(y_train[0])
# print(boxs[1][0])