# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="3"
import dataP
import modelP
from keras.models import load_model
import fileP
from keras import utils
import numpy as np
import time
############创建模型

stime = time.time()
# # model =load_model("test1-5x8")a
model = modelP.createModel()
print("模型准备完成")
###########获取文件名称列表
namelist =fileP.filelist("data/")
print("数据路径装填成功")
# ###########20折交叉验证
test = 0
fold = 39
cir = 6
print("开始20折交叉验证")
for shana in range(0,cir):
    count = 0
    for i in range(0,fold):
        if(test <=12):
            if(i == test*2 or i == test*2+1):
                continue
        else:
            if(test == 13):
                if(i == test*2):
                    continue
            else:
                if(i == test*2 or i == test*2 -1):
                    continue
        count = count+1
        print(str(shana)+"-"+str(count)+":")
        x,y,n = dataP.gettrain(namelist[0][i],namelist[1][i])
        # print(namelist[0][i])
        f = open(namelist[0][i])
        print("数据准备完成")
        x = np.expand_dims(x,axis=2)
        # print(x.shape)
        y = utils.to_categorical(y)
        print("开始验证")
        model.fit(x,y,epochs=8, batch_size=n,shuffle=True,validation_split=0.21)
model.save("2-test"+str(test)+"-"+str(cir)+"x8")


# print(namelist[0][test])
# for test in range(0,1):
a = test * 2
flag = 1
if (test <= 12):
    b = test * 2 + 1
else:
    if (test == 13):
        flag = 0
        b = -1
    else:
        b = test * 2 - 1
print(str(a) + "---" + str(b))
testx1, testy1, uu = dataP.gettest(namelist[0][a], namelist[1][a])
if (flag == 1):
    testx2, testy2, uu2 = dataP.gettest(namelist[0][b], namelist[1][b])
    testx = np.concatenate((testx1, testx2))
    testy = np.concatenate((testy1, testy2))
else:
    testx = testx1
    testy = testy1
testx = np.expand_dims(testx, axis=2)
testy = utils.to_categorical(testy)
loss,acc = model.evaluate(testx,testy)
print("Loss: "+str(loss))
print("Acc: "+str(acc))
etime = time.time()
print("Time: "+str(etime-stime))


