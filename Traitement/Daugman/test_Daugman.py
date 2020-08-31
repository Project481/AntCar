# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 11:17:45 2020

@author: Florentin
"""

from Algo_Daugman import daugman
from Algo_Daugman import find_iris
import skimage.io as io
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
import math

f = io.imread("D:\PFE\Illustrations\Test detection\DB_test9.jpg")
f=f[:,:,0]+f[:,:,1]+f[:,:,2]
f_square=f[:,128:-128]

#f_square=np.concatenate((f, np.zeros((1024-768,1024))),0) 
debut=time.time()
size=f_square.shape
res = cv2.resize(f_square, dsize=(int(size[0]/5),int(size[1]/5)), interpolation=cv2.INTER_CUBIC)
x_rough=find_iris(res,30,50,int(size[0]/10),int(size[0]/10))

xc,yc=x_rough[0]
cv2.circle(res,(xc,yc), x_rough[1], (0,255,0), 1)
cv2.circle(res,(xc,yc), int(x_rough[1]/4.44), (0,255,0), 1)
plt.imshow(res)

cx_rough,cy_rough=x_rough[0]
x_fin=find_iris(f_square,x_rough[1]*5-10,x_rough[1]*5+10,cx_rough*5,cy_rough*5)

print(time.time()-debut)
xc,yc=x_fin[0]
cv2.circle(f_square,(xc,yc), x_fin[1], (0,255,0), 5)
cv2.circle(f_square,(xc,yc), int(x_fin[1]/4.44), (0,255,0), 5)
plt.figure()
plt.imshow(f_square)


