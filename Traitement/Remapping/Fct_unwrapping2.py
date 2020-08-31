# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 10:13:14 2020

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
image = io.imread("F:\image1593165678.11.tiff")

Cx=315
Cy=235
Re=115
Ri=24




def LookUpTable(Cx,Cy,Re,Ri):
    # Crée un dictionnaire qui pour toute coordonnée de l'image déroulée associe une coordonnée de l'image de départ

    #global Passage,Panorama,width,W
    width=int(Re-Ri)
    W=int(2*math.pi*Re)
    IndX=numpy.zeros((width,W),dtype=numpy.int)
    
    IndY=numpy.zeros((width,W),dtype=numpy.int)
    # Pour chaque point du panorama, on recherche ses coordonnées dans le repère polair
    for Xunwrap in range(int(W)):
        for Yunwrap in range(int(width)):

            Xorig=(Ri+Yunwrap)*math.cos(-Xunwrap/Re)+Cx
            Yorig=(Ri+Yunwrap)*math.sin(-Xunwrap/Re)+Cy
            
            IndX[(Yunwrap,Xunwrap)]=int(Xorig)
            IndY[(Yunwrap,Xunwrap)]=int(Yorig)
    return IndX,IndY,width,W


def unwrap2(image,IndX,IndY,width,W):
    debut=time.time()
    Panorama=image[IndY,IndX]

    duree=time.time()-debut
    print(duree)
    return Panorama
