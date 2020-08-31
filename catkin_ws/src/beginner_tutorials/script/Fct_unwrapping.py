# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 14:47:29 2020

@author: Florentin
"""

import scipy
import math
import numpy
import time

def LookUpTable(Cx,Cy,Re,Ri):
    # Fonciton qui prend en arguments les caracteristiques d'un disque et renvoie deux matrices
    # Entree : coordonnees du centre (x,y), rayon exterieur, rayon interieur

    # Calcul des dimensions de l'image deroulee
    width=int(Re-Ri)
    W=int(2*math.pi*Re)
    # Initialisation des matrices retournes
    IndX=numpy.zeros((width,W),dtype=numpy.int)
    IndY=numpy.zeros((width,W),dtype=numpy.int)

    # Pour chaque point du panorama, on recherche ses coordonnées dans le repère polair
    for Xunwrap in range(int(W)):
        for Yunwrap in range(int(width)):
            # Determination de la position du pixel dans l'image d'origine a partir d'une position dans l'image deroulee
            Xorig=(Ri+Yunwrap)*math.cos(-Xunwrap/Re+math.pi)+Cx
            Yorig=(Ri+Yunwrap)*math.sin(-Xunwrap/Re+math.pi)+Cy

            # La position du pixel dans l'image d'origine est stockee dans deux matrices
            IndX[(Yunwrap,Xunwrap)]=int(Xorig)
            IndY[(Yunwrap,Xunwrap)]=int(Yorig)
    return IndX,IndY
