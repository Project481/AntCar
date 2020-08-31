# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 09:46:25 2020

@author: Florentin
"""

import skimage.io as io
import matplotlib.pyplot as plt
import numpy
import skimage.morphology
import skimage.feature
import colorsys
import time
import scipy
import math

f = io.imread("test1.jpg")
t_init=time.time()
f=f/255
Cx=510
Cy=307
re=182
ri=41
width=re-ri
W=2*math.pi*(width)
Panorama=scipy.zeros((int(width),int(W),3))
Parcours=[]
for Xunwrap in range(int(W)):
    for Yunwrap in range(int(width)):
        #if math.pow(Xorig-Cx,2)+math.pow(Yorig-Cy,2)<math.pow(r,2):
            Xorig=(re-Yunwrap)*math.cos(Xunwrap/(width))+Cx
            Yorig=(re-Yunwrap)*math.sin(Xunwrap/(width))+Cy
            
            
            Panorama[Yunwrap,Xunwrap]=f[int(Yorig),int(Xorig)]
        
# =============================================================================
#             f[int(Yorig),int(Xorig),0]=0
#             f[int(Yorig),int(Xorig),1]=0
#             f[int(Yorig),int(Xorig),2]=255
# =============================================================================

duree=time.time()-t_init

plt.imshow(Panorama,cmap='gist_gray')