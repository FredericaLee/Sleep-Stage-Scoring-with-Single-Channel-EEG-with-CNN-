import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

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
    s = open("C:/Users/win/Desktop/SC4001E0-PSG_data.txt")
    count = 0
    inct = 0
    listsum = []
    listtemp = []
    while(1):
        temp = s.readline()
        count = count + 1
        if(count <3057002):
            continue
        #if(count > 3057005):
        if(count >5232001):
            break
        #print(temp)
        num = float(temp.split(",")[1])
        #print(num)
        tt = np.array([num])
        listtemp.append(copy.deepcopy(tt))
        inct = inct + 1
        if(inct == 3000):
            listsum.append(copy.deepcopy(listtemp))
            listtemp = []
            inct  = 0
    re = []
    test = []
    #print(len(listsum))
    for i in range (0,721):
        #print(i)
        #tempnp = np.array(listsum[i]+listsum[i+1]+listsum[i+2]+listsum[i+3]+listsum[i+4])
        tempnp = listsum[i] + listsum[i + 1] + listsum[i + 2] + listsum[i + 3] + listsum[i + 4]
        tempnp = np.array(tempnp)
        #print(len(tempnp))
        if (i%20 != 0):
            re.append(copy.deepcopy(tempnp))
        else:
            test.append(copy.deepcopy(tempnp))
    return np.array(re),np.array(test)

def getL():
    f = open("C:/Users/win/Desktop/labels.txt")
    y = []
    test = []
    for i in range(0,721) :
        temp = f.readline()
        if(temp =="W\n"):
            temp = "0"
        if(temp =="R\n"):
            temp = "4"
        if(i%20 != 0):
            y.append(copy.deepcopy(temp))
        else:
            test.append(copy.deepcopy(temp))
    return np.array(y),np.array(test)



x_train,x_test = getV()
y_train,y_test = getL()

y_train = utils.to_categorical(y_train)
y_test  = utils.to_categorical(y_test)
#print(x_test)
# print(len(x_train))
# print(len(x_test))
# print(len(y_train))
# print(len(y_test))
# print(y_test[36])
#############################定义网络##############################
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

model.add(Conv2D(filters=400, kernel_size = (20,30), strides= 1,padding = 'valid',activation='relu'))
print("C2：",end="")
print(model.output_shape)
model.add(MaxPooling2D(pool_size=(1,10), strides=2, padding='valid'))
print("P2：",end="")
print(model.output_shape)

model.add(Flatten())
print(model.output_shape)

model.add(Dense(500,activation='relu'))
print("M1：",end="")
print(model.output_shape)
model.add(Dense(500,activation='relu'))
print("M2：",end="")
print(model.output_shape)

model.add(Dense(5,activation='softmax'))
print(model.output_shape)

model.compile(optimizer=opt.SGD(),loss='categorical_crossentropy',metrics=['accuracy'])


#############################训练网络##############################
model.fit(x_train,y_train,batch_size=1,epochs= 5,verbose= 2,validation_split=0.21,shuffle=True)

loss,acc = model.evaluate(x_test,y_test)
print("loss =",loss)
print("acc = ",acc)

# print("Duaration:"+str(edf.getFileDuration()))
# print("Freq.:"+str(edf.getSampleFrequencies()))
# print("N-Sample(=Freq x Duaration):"+str(edf.getNSamples()))
# print("Date:"+str(edf.getStartdatetime()))
# plt.plot(edf.readSignal(0)[0:1000],label=labels[0])
# plt.plot(edf.readSignal(1)[0:1000],label=labels[1])
# plt.plot(edf.readSignal(2)[0:1000],label=labels[2])
# plt.legend()
# plt.show()



# data = np.random.random((1000, 100))
# print(data)


