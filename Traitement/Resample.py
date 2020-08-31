# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 09:31:46 2020

@author: Florentin
"""

def resample(Image,resolution):
    # La fonction resample prend en arguments Image et resolution et renvoie Im_resample
    # Resolution est la resolution souhaitée en °/px
    import scipy
    import numpy
    
    # Nb de pixel de l'image rééchantillonnée
    px_Lig=82//resolution
    px_Col=360//resolution
    
    # Image rééchantillonnée
    Im_resampled=scipy.zeros((px_Lig,px_Col,3))
    
    # Taille sous-tableau (Ech) de px moyennés
    Ech_Lig=Image.shape[0]//px_Lig
    Ech_Col=Image.shape[1]//px_Col
    
    # Taille maximale pour avoir le même nombre de px moyenné en ligne et colonne
    Ech_max=min(Ech_Lig,Ech_Col)
    
    for i in range(px_Lig):
        for j in range(px_Col):
            # Selection de l'échantillon à moyenner
            ech=Image[i*Ech_max:(i+1)*Ech_max,j*Ech_max:(j+1)*Ech_max,:]
            # Moyenne des intensités du sous-tableau sur (r,g,b)
            px=numpy.mean(numpy.mean(ech,1),0)
            # Remplir l'image rééchantillonnée
            Im_resampled[i,j]=px
            
            
    return Im_resampled