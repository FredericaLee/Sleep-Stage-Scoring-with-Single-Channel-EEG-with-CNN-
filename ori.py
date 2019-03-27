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
import numpy as np
from keras import utils
import copy


#############################准备数据##############################

def getV():
    s = open("SC4001E0-PSG-EegData.txt")
    #s = open("I:/data/StructedDataAndLabel_20170620(Fpz-Cz)/SC4001E0-PSG-EegData.txt")
    ct = []
    re = []
    test = []
    listsum = []
    for i in range (0,1742):
        temp = s.readline()
        if(i<1019):
            continue
        tempnp = temp.split("\t")
        for j in range(0,len(tempnp)):
            tempnp[j] =np.array([ float(tempnp[j])])
        print(type(tempnp[0]))
        listsum.append(copy.deepcopy(tempnp))

    for i in range(0,1740):
        if(i<1021):
            continue
        tempnps = np.array(listsum[i-1021]+listsum[i-1020]+listsum[i-1019]+listsum[i-1018]+listsum[i-1017])
        if (i%20 != 0):
            re.append(copy.deepcopy(tempnps))
        else:
            ct.append(i+2)
            test.append(copy.deepcopy(tempnps))
    return np.array(re),np.array(test),ct
# 0-W-0 1-N1-1 2-N2-2 3-N3/N4-3/4 4-R-5
def getL():
    f = open("SC4001E0-PSG-EegLabel.txt")
    #f = open("I:/data/StructedDataAndLabel_20170620(Fpz-Cz)/SC4001E0-PSG-EegLabel.txt")
    y = []
    test = []
    ct = []
    temp = f.readline()
    temp = f.readline()
    for i in range(0,1740) :
        temp = f.readline()
        if(i<1021):
            continue
        temp = int(temp)
        if(temp == 4):
            temp = 3
            #print(str(i)+"N3")
        if(temp == 5):
            temp = 4
            #print(i)
        if(i%20 != 0):
            y.append(copy.deepcopy(temp))
        else:
            test.append(copy.deepcopy(temp))
            ct.append(i)
    return np.array(y),np.array(test),ct
#
x_train,x_test,x_num= getV()
# print(len(x_train[2512]))
# print(len(x_train))
# print(len(x_test))
y_train,y_test,y_num = getL()
# print(len(y_train))
# print(len(y_test))
# print(x_num)
# print(y_num)
y_train = utils.to_categorical(y_train)
y_test  = utils.to_categorical(y_test)
#
# np.save("xtrain.npy",x_train)
# np.save("xtest.npy",x_test)
# np.save("ytrain.npy",y_train)
# np.save("ytest.npy",y_test)
# print(x_train.shape)
# print(x_test.shape)
# print(y_train.shape )
# print(y_test.shape )
#print(x_test)
# print(len(x_train))
# print(len(x_test))
# print(len(y_train))
# print(len(y_test))
# print(y_test[36])

# x_train = np.load("xtrain.npy")
# x_test = np.load("xtest.npy")
# y_train = np.load("ytrain.npy")
# y_test = np.load("ytest.npy")
# #############################定义网络##############################
# model = Sequential()
# #(1,1,15000)    每一个数据是一个1维数据
# model.add(Conv1D(filters=20, kernel_size = 200, strides= 1,padding = 'valid', input_shape=(15000,1),activation='relu'))
# print(model.input_shape)
# print("C1：",end="")
# print(model.output_shape)
# #15000-199(移动199次
# #(20,1,14801)   每一个数据是一个1维数据，只是一个epoch上取了20个数据
# model.add(MaxPooling1D(pool_size=20, strides=10, padding='valid'))
# print("P1：",end="")
# print(model.output_shape)
# #(20,1,1479)（数据变为原来的1/10
# #stacking, h201d变为h1 的20维数据
# #stacking layer
# print("Stacking layer：",end="")
# model.add(Reshape([20,-1,1]))
# print(model.output_shape)
#
# model.add(Conv2D(filters=400, kernel_size = (20,30), strides= 1,padding = 'valid',activation='relu',data_format='channels_last'))
# print("C2：",end="")
# print(model.output_shape)
# model.add(MaxPooling2D(pool_size=(1,10), strides=2, padding='valid',data_format='channels_last'))
# print("P2：",end="")
# print(model.output_shape)
#
# model.add(Flatten())
# print(model.output_shape)
#
# model.add(Dense(500,activation='relu'))
# print("M1：",end="")
# print(model.output_shape)
# model.add(Dense(500,activation='relu'))
# print("M2：",end="")
# print(model.output_shape)
#
# model.add(Dense(5,activation='softmax'))
# print(model.output_shape)
#
# model.compile(optimizer=opt.SGD(),loss='categorical_crossentropy',metrics=['accuracy'])
#
#
# #############################训练网络##############################
# model.fit(x_train,y_train,epochs= 5)
#
# loss,acc = model.evaluate(x_test,y_test)
# print("loss =",loss)
# print("acc = ",acc)

# # print("Duaration:"+str(edf.getFileDuration()))
# # print("Freq.:"+str(edf.getSampleFrequencies()))
# # print("N-Sample(=Freq x Duaration):"+str(edf.getNSamples()))
# # print("Date:"+str(edf.getStartdatetime()))
# # plt.plot(edf.readSignal(0)[0:1000],label=labels[0])
# # plt.plot(edf.readSignal(1)[0:1000],label=labels[1])
# # plt.plot(edf.readSignal(2)[0:1000],label=labels[2])
# # plt.legend()
# # plt.show()

# # data = np.random.random((1000, 100))
# # print(data)
