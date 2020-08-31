# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 16:11:48 2020

@author: Florentin
"""
from Fct_unwrapping import unwrap
from Resample import resample

import skimage.io as io
import matplotlib.pyplot as plt
import numpy
import skimage.morphology
import skimage.feature
import colorsys
import time
import scipy
import math
import cv2

f = io.imread("D:\PFE\Illustrations\Traitement d'image\Samples detection\DB_test2.jpg")
f=f/255
Cx=493
Cy=358
re=188
ri=42

Panorama=unwrap(f,Cx,Cy,re,ri)
plt.imshow(f)
plt.figure()
plt.imshow(Panorama)
for resolution in [1,5,10]:
    print(resolution)
    final_size=(int(360/resolution),int(82/resolution))
    Panorama_resampled=cv2.resize(Panorama,final_size,interpolation = cv2.INTER_NEAREST)
    #Panorama_resampled=resample(Panorama,10)
    

    plt.figure() 
    plt.imshow(Panorama_resampled) 










