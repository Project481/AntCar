# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:23:32 2020

@author: Florentin
"""





from Fct_unwrapping import unwrap
from Resample import resample

import skimage.io as io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy
import skimage.morphology
import skimage.feature
import colorsys
import time
import scipy
import math
import cv2
from PIL import Image

for i in range(1,33,1):
    f = io.imread("D:\PFE\Test2905\Zigzag\Raw\image" + str(i) + ".jpg")
    
    f=f/255
    
    panorama=unwrap(f,500,336,192,41)
    panorama=(panorama[:,:,0]+panorama[:,:,1]+panorama[:,:,2])/3

    im = Image.fromarray(panorama)
    mpimg.imsave("Panorama_Zigzag" + str(i) + ".jpg",im,cmap='gray')



# panorama_zoom=panorama[:,300:600]
# panorama_rect = cv2.rectangle(panorama_zoom, (140,50), (160,100),(0, 0, 0) , 3) 
# plt.imshow(panorama_rect)
# # panorama_grey=(panorama[:,:,0]+panorama[:,:,1]+panorama[:,:,2])/3
# # plt.imshow(panorama_grey,cmap="Greys")



