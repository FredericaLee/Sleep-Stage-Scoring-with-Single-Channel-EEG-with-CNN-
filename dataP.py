import numpy as np
import copy
import math

###所有计数从1开始
#0-W   1-N1 2-N2  3-N3 4-R
def LP(name):                                   #从文件中获取label
    # f = open("SC4001E0-PSG-EegLabel.txt")
    f = open(name)
    ct = 0                                      #标识当前到哪了(总文件里的内容)
    start = 3                                 #有用段的起始位置----总文件的坐标
    lastnz = 0                                  #记住当前最后一个非零的位置，也即是有用段的结束位置----总文件里的坐标
    labels = []                                 #保存所有有用label的
    while(1):
        ct = ct +1
        temp = f.readline()
        # if (start==0 and temp != "0\n" ):         #第一个不是0的位置：
        #     start = ct

        #####寻找有用段的起始位置
        if (start != -1):
            if(temp == "3\n" or temp =="4\n"):
                labels.append("3")
            else:
                if (temp == "5\n"):
                    labels.append("4")
                else:
                    labels.append(temp)
            if(temp == "6\n"):
                ct = ct -1
                lastnz = ct
                break
    #####提取有用段的label
    label = []
    count  = [[],[],[],[],[]]
    cct = 0                                     #标识到有用段的位置
    for i in range (0,lastnz-start-1):
        cct = cct + 1
        # print(str(cct)+":")
        label.append(labels[i])
        if (labels[i] == "0\n" or labels[i]=="0"):
            # print("0")
            count[0].append(cct)
        else:
            if (labels[i] == "1\n" or labels[i] == "1"):
                # print("1")
                count[1].append(cct)
            else:
                if (labels[i] == "2\n" or labels[i] == "2"):
                    # print("2")
                    count[2].append(cct)
                else:
                    if (labels[i] == "3" or labels[i]=="3\n"):
                        # print("3")
                        count[3].append(cct)
                    else:
                        if (labels[i] == "4" or labels[i] == "4\n"):
                            # print("4")
                            count[4].append(cct)
    # label = np.array(label)
    # print(label.shape)
    return label,count,start,lastnz

def LD(start,end,name):
    # f =open("SC4001E0-PSG-EegData.txt")
    f = open(name)
    ct = 0                                  #用于标志总文件里的坐标
    rawdata = []
    data = []
    while(1):
        ct = ct + 1
        temp = f.readline()
        if(ct <start-2):                    #因为需要前两个的数据
            continue
        if(ct>end):
            break
        templ =np.array(temp.split("\t"))
        tempp =[]
        for i in range(0,len(templ)):
            tempp.append(float(templ[i]))
        # print(tempp.shape)
        rawdata.append(copy.deepcopy(tempp))

    ####合成最终的数据
    for i in range(0,len(rawdata)-4):
        temp = np.array(rawdata[i]+rawdata[i+1]+rawdata[i+2]+rawdata[i+3]+rawdata[i+4])
        data.append(copy.deepcopy(temp))

    # data = np.array(data)
    #print(data.shape)
    return data

def Box(data,label,count):
    redata  = []
    relabel = []
    lenlist = []
    torilist = []
    for i in range(0,len(count)):
        lenlist.append(len(count[i]))

    batchsize = 5 * min(lenlist)
    index = [0,0,0,0,0]                     #用于读取各个count位
    n = math.ceil(max(lenlist)/min(lenlist))

    for i in range(0,n):                    #循环n次，有n个batch
        for j in range(0,5):                #对于5个类别，j代表类别
            for k in range(0,min(lenlist)): #取min个数据
                torilist.append(count[j][index[j]])
                index[j] =(index[j]+1)%len(count[j])

    # print(n)
    # print(min(lenlist))
    # print(batchsize)
    # print(batchsize*n)
    # print(len(torilist))

    for i in range(0,len(torilist)):
        # print(torilist[i]-1)
        redata.append(data[torilist[i]-1])
        relabel.append(label[torilist[i]-1])
    # xx =torilist[8]
    redata = np.array(redata)
    relabel = np.array(relabel)
    return redata,relabel,batchsize#,xx



def gettrain(name1,name2):
    label,count,start,end = LP(name2)
    # print("标签数据装载")
    # print(start)
    # print(end)
    data = LD(start,end,name1)
    # print("egg数据装载")
    # print(data.shape)
    # print(type(data[0]))
    # print(type(data[0][0]))
    redata,relabel,batchsize = Box(data,label,count)
    # print("分类完成")
    # print(label[xx - 1])
    # print(data[xx - 1])
    # print(xx)
    return redata,relabel,batchsize


def gettest(name1,name2):
    label, count, start, end = LP(name2)
    data = LD(start, end, name1)
    label = np.array(label)
    data = np.array(data)
    return data,label,128


# gettrain("SC4001E0-PSG-EegData.txt","SC4001E0-PSG-EegLabel.txt")
# data,label,size = get()
# print("X============================")
# print(len(data))
# print(len(data[0]))
# print(data.shape)
# print(type(data[0]))
# print(type(data[0][0]))
# print("")
#
# print("y=============================")
# print(len(label[0]))
# print(label.shape)
# print(type(label[0]))
# print("")
# print("AXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


