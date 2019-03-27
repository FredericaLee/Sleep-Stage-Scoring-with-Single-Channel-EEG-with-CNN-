import math
import numpy as np
import copy

np.set_printoptions(threshold=np.inf)
def getLabel():
    tar = open("C:/Users/win/Desktop/labels.txt","w+")
    s = open("C:/Users/win/Desktop/SC4001EC-Hypnogram_annotations.txt")
    count = 0
    countw = []
    countr = []
    count1 = []
    count2 = []
    count3 = []
    listlabel = []
    flag = 0
    start = 0
    end  =0
    nums = 0
    tlabel=""
    while(1):
        line = s.readline()
        count = count+1
        #print("line: "+str(count))
        if(count == 1 or count==2):
            continue
        temp =  line.split(",")     #[52260.00000][Sleep Stage 1]
        #print(temp)
        num = float(temp[0].split("+")[1])         #[526000]
        n = int((num-nums)/30)               #有几个对应的stage
        #print("次数："+str(n))
        #print(num)
        labels =((temp[1]).split(" "))[2]       #[1]
        if((labels > "?\n") - (labels < "?\n") == 0):
            flag = 1
            end = nums
            n=0
        if(count == 3 ):
            tlabel = labels
            nums = num
            start = nums
            #print(nums)
            continue
        count = count -1
        #print("L:"+tlabel)
        nums = num
        for i in range(0,n):          #循环写入stage
           if( (tlabel>"4\n")-(tlabel<"4\n") == 0 or (tlabel>"3\n")-(tlabel<"3\n") == 0):
                tar.write("3\n")
                listlabel.append(3)
                count3.append(count-2)
           else:
               if((tlabel>"2\n")-(tlabel<"2\n") == 0):
                    tar.write(tlabel)
                    listlabel.append(2)
                    count2.append(count-2)
               else:
                   if ((tlabel > "1\n") - (tlabel < "1\n") == 0):
                       tar.write(tlabel)
                       count1.append(count-2)
                       listlabel.append(1)
                       #print(count-2)
                   else:
                       if ((tlabel > "W\n") - (tlabel < "W\n") == 0):
                           tar.write(tlabel)
                           countw.append(count-2)
                           listlabel.append(0)
                       else:

                           if ((tlabel > "R\n") - (tlabel < "R\n") == 0):
                               tar.write(tlabel)
                               countr.append(count-2)
                               listlabel.append(4)
                           else:
                               if ((tlabel > "?\n") - (tlabel < "?\n") == 0):           #?直接跳出
                                   flag = 1
                                   print(1)
                                   break
                               else:                                                    #move,计数加，即为NA——即不用
                                   tar.write("NA")
                                   listlabel.append(5)
           count = count + 1
        tlabel = labels
        if (flag == 1):
            break
    #print(countr)
    #print(len(countr))
    return countr,count1,count2,count3,countw,start,end,listlabel
#getLabel()

def getV(start,end):

    s = open("C:/Users/win/Desktop/SC4001E0-PSG_data.txt")
    count = 0
    inct = 0
    listsum = []
    listtemp = []
    while(1):
        temp = s.readline()
        count = count + 1
        if(count <(start-60)/0.01+2):

            continue
        #if(count > 3057005):
        if(count >(end+60)/0.01+1):
            break
        #print(temp)
        num = float(temp.split(",")[1])
        #print(num)
        listtemp.append(num)
        inct = inct + 1
        if(inct == 3000):
            listsum.append(copy.deepcopy(listtemp))
            listtemp = []
            inct  = 0
    re = []
    #print(len(listsum))
    #print(int((end-start)/30))
    for i in range (0,int((end-start)/30)):#如果要加入前后2个阶段的数据的话
        #print(i)
        tempnp = np.array(listsum[i]+listsum[i+1]+listsum[i+2]+listsum[i+3]+listsum[i+4])
        #print(len(tempnp))
        re.append(copy.deepcopy(tempnp))
    return re

def Box(countr, count1, count2, count3, countw):
    lenlist = []
    lenlist.append(len(countr))
    lenlist.append(len(count1))
    lenlist.append(len(count2))
    lenlist.append(len(count3))
    lenlist.append(len(countw))
    lis = [countr,count1,count2,count3,countw]
    xt = min(lenlist)
    xm = max(lenlist)
    xtindex = lenlist.index(xt)
    n = math.ceil(xm/xt)
    boxs = []
    index=[0,0,0,0,0]
    for i in range(0,n):                #一共N个组
        mem = []
        for j in range(0,5):            #每个组对存着不同分期的列表进行循环
            if(j == xtindex):           #是最少的，直接加进去
                mem.extend(lis[j])
            else:                       #不是最少的，开始循环读取xt个数据
                for k in range(0,xt):
                    mem.append(lis[j][index[j]])
                    index[j] = (index[j]+1)%len(lis[j])

        boxs.append(copy.deepcopy(mem))

    return boxs


def BoxV(boxs,re,listlable):
    batchD = []
    lable = []
    for i in range(0,len(boxs)):#对每个盒子进行书写数据
        # name = "box"+str(i)
        # f = open("C:/Users/win\Desktop/test/"+name, mode='w+')
        #print(boxs[i]# )
        tempbox = []
        templable = []

        for j in range(0,len(boxs[i])):
        #for j in range(0, 1):
            #temp =" ".join(re[boxs[i][j]-
            #print(boxs[i][j]-1)
            temp = re[boxs[i][j]-1]
            tempbox.append(temp)
            temp2 = int(listlable[boxs[i][j]-1])
            templable.append(temp2)
            # f.write(temp+"\n")
        batchD.append(tempbox)
        lable.append(templable)
    return batchD,lable


countr, count1, count2, count3,countw,start,end,listlable = getLabel()
# re = getV(start,end)
# boxs = Box(countr,count1,count2,count3,countw)
# lable,data =BoxV(boxs,re,listlable)
# label =BoxL(boxs)

print(len(countw))
print(len(count3))
print(len(count1))
# print(len(lable))
# print(len(lable[0]))
# print(len(lable[4]))
# print(lable[0][0])
# print(boxs[0][0])
# print(data[0][0])

# countr, count1, count2, count3,countw,start,end,listlable = getLabel()
# re = getV(start,end)
# boxs = Box(countr,count1,count2,count3,countw)
# data,lable =BoxV(boxs,re,listlable)
# print("数据准备完成")
# np.save("data.npy",data)
# np.save("label.npy",lable)


