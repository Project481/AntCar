# -*- coding: utf-8 -*-
"""
Created on Fri May 15 15:31:12 2020

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



Contraste=numpy.zeros(50)
Periode=numpy.arange(35,281,5)
Frequences=40*math.pi/(Periode*180)
for i in range(5):
    
    f = io.imread("D:\PFE\Illustrations\Filtrage Passe-Bas\Horizontale\FTM Horizontale mire FINE\Mire_H_F_" + str(Periode[i]) + ".png")
    
    f=f/255
    
    f=(f[:,:,0]+f[:,:,1]+f[:,:,2])/3
    Contraste[i]=numpy.amax(f)-numpy.amin(f)
    

plt.plot(Frequences,Contraste)
    
    