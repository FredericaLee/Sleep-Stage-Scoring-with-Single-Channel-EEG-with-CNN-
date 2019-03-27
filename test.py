# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="5"
import dataP
import modelP
from keras.models import load_model
import fileP
from keras import utils
import numpy as np
import time
############创建模型

stime = time.time()
# model =load_model("test1-5x8")
model = modelP.createModel()
print("模型准备完成")
###########获取文件名称列表
namelist =fileP.filelist("data/")
# print("数据路径装填成功")
# ###########20折交叉验证
test = 19
fold = 20
cir = 6
print("开始"+str(fold)+"折交叉验证")
for shana in range(0,cir):
    count = 0
    for i in range(0,20):
        if(i == test):
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


print(namelist[0][test])
testx,testy, uu= dataP.gettest(namelist[0][test],namelist[1][test])
testx = np.expand_dims(testx,axis=2)
testy = utils.to_categorical(testy)
loss,acc = model.evaluate(testx,testy)
print("Loss: "+str(loss))
print("Acc: "+str(acc))
etime = time.time()
print("Time: "+str(etime-stime))
# print(y.shape)



