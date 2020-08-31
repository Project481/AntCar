# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 14:47:29 2020

@author: Florentin
"""


import scipy
import math

def unwrap(image,Cx,Cy,Re,Ri):
    
    import scipy
    import math
    width=Re-Ri
    W=2*math.pi*Re
    # Définition du tableau contennant le panorama
    Panorama=scipy.zeros((int(width),int(W),3))
    # Pour chaque point du panorama, on recherche ses coordonnées dans le repère polair
    for Xunwrap in range(int(W)):
        for Yunwrap in range(int(width)):
            
            Xorig=(Ri+Yunwrap)*math.cos(-Xunwrap/Re)+Cx
            Yorig=(Ri+Yunwrap)*math.sin(-Xunwrap/Re)+Cy
            
            Panorama[Yunwrap,Xunwrap]=image[int(Yorig),int(Xorig)]
    
    return Panorama
    