#import
import time as t, random as r, numpy as np

#import numpy as np
tstart = t.time()
#Uni  = np.full((255,1), None)
Uni = [0] * 256
#0  1   2   3   4   5   6   7       Device_1
#8  9   10  11  12  13  14  15      Device_2
#16 17  18  19  20  21  22  23      Device_2

dev_1 = ["_1_"] * 8
dev_2 = ["_2_"] * 8
dev_3 = ["_3_"] * 8
Uni[0:7]= dev_1
Uni[8:15]= dev_2
Uni[16:23]= dev_3
print(dev_1, "\n",dev_2, "\n",dev_3, "\n")

def Refresh():
    global Uni
    Uni[0:7]= dev_1
    Uni[8:15]= dev_2
    Uni[16:23]= dev_3


def All_Fill_RGB(R,G,B):
    global Uni
    Uni[0:2]      = [R,G,B]
    Uni[8:10]     = [R,G,B]
    Uni[16:18]    = [R,G,B]
    print(Uni)

def Fill_RGB_random(dev1,dev2,dev3):
    global dev_1,dev_2,dev_3

    R = r.randint(0, 255)  
    G = r.randint(0, 255)  
    B = r.randint(0, 255)  

    if(dev1==1):
        dev_1[0:2]      = [R,G,B]
    if(dev2==1):
        dev_2[8:10]     = [R,G,B]
    if(dev3==1):
        dev_3[16:18]    = [R,G,B]

    Refresh()
    print(Uni)

def Push():
    

#print(Uni)
All_Fill_RGB(256,2,3)
#Fill_RGB_random(1,1,1)


#print("JoanhDerSCHLINGEL<3")


print(t.time()-tstart)
