#!/usr/bin/env python3
import cv2
import numpy
import matplotlib.pyplot as plt
import time
def DetectionCouronne(img):
    # Fonction qui prend en argument une image en niveaux de gris codee sur 8 bits.
    # La fonction retourne les parametres de la meilleure couronne trouvee sur l'image
    # En sortie : tableau contenant les coordonnees du centre, le rayon exterieur et interieur
    # [Cx,Cy,R,r]


    # Definition des bornes de l'intervalle de recherche du cercle exterieur et interieur
    Rmax=int(img.shape[0]/2)
    Rmin=int(img.shape[0]/5)

    rmax=int(Rmax/4.5)
    rmin=int(Rmin/4.5)


    # Transformee de Hough pour le cercle exterieur
    circles_ext = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,1,param1=50,param2=30,minRadius=Rmin,maxRadius=Rmax)
    circles_ext = numpy.uint(numpy.around(circles_ext))


    # Transformee de Hough pour le cercle interieur
    circles_int = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,1,param1=50,param2=30,minRadius=rmin,maxRadius=rmax)
    circles_int = numpy.uint(numpy.around(circles_int))

    MaxValue=float('-inf')
    BestDisques=[0,0,0,0,0,0]

    Value=0

    # On selectionne au maximum 10 cercles exterieurs et interieurs
    nb_cercle_ext=circles_ext.shape[1]
    nb_cercle_int=circles_int.shape[1]
    if circles_ext.shape[1]>10:
        nb_cercle_ext=10
    if circles_int.shape[1]>10:
        nb_cercle_int=10

    # On choisit le centre des cercles exterieurs comme centre des couronnes
    for i in range(nb_cercle_ext):
        for j in range(nb_cercle_int):

            # Creation d'un masque pour selectionner les pixels a l'exterieur du cercle exterieur
            Mask_ext=numpy.ones(img.shape)
            Mask_ext=cv2.circle(Mask_ext, (circles_ext[0,i,0],circles_ext[0,i,1]), circles_ext[0,i,2], 0, -1)

            # Creation d'un masque pour selectionner les pixels a l'interieur du cercle interieur
            Mask_int=numpy.zeros(img.shape)
            Mask_int=cv2.circle(Mask_int, (circles_ext[0,i,0],circles_ext[0,i,1]), circles_int[0,j,2], 1, -1)

            # Creation d'un masque pour selectionner les pixels dans la couronne
            Mask_ring=numpy.zeros(img.shape)
            Mask_ring=cv2.circle(Mask_ring, (circles_ext[0,i,0],circles_ext[0,i,1]), circles_ext[0,i,2], 1, -1)
            Mask_ring=cv2.circle(Mask_ring, (circles_ext[0,i,0],circles_ext[0,i,1]), circles_int[0,j,2], 0, -1)

            # Calcul d'un indice qui est maximum si l'image est une couronne parfaite (couronne blanch et reste noir) et de parametre [circles_ext[0,i,0],circles_ext[0,i,1],circles_ext[0,i,2],circles_int[0,j,2]]
            Value=numpy.sum(numpy.multiply(img,Mask_ring)/numpy.sum(Mask_ring)-numpy.multiply(img,Mask_ext)/numpy.sum(Mask_ext)-numpy.multiply(img,Mask_int)/numpy.sum(Mask_int))
            # Mise a jour du meilleur indice et disque courant
            if Value>MaxValue:
                BestDisques=[circles_ext[0,i,0],circles_ext[0,i,1],circles_ext[0,i,2],circles_int[0,j,2]]
                MaxValue=Value


    # On choisit le centre des cercles interieur comme centre des couronnes
    for i in range(nb_cercle_int):
        for j in range(nb_cercle_ext):

            Mask_ext=numpy.ones(img.shape)
            Mask_ext=cv2.circle(Mask_ext, (circles_int[0,i,0],circles_int[0,i,1]), circles_ext[0,j,2], 0, -1)
            # Selectionner les pixels a l'interieur
            Mask_int=numpy.zeros(img.shape)
            Mask_int=cv2.circle(Mask_int, (circles_int[0,i,0],circles_int[0,i,1]), circles_int[0,i,2], 1, -1)


            Mask_ring=numpy.zeros(img.shape)
            Mask_ring=cv2.circle(Mask_ring, (circles_int[0,i,0],circles_int[0,i,1]), circles_ext[0,j,2], 1, -1)
            Mask_ring=cv2.circle(Mask_ring, (circles_int[0,i,0],circles_int[0,i,1]), circles_int[0,i,2], 0, -1)

            Value=numpy.sum(numpy.multiply(img,Mask_ring)/numpy.sum(Mask_ring)-numpy.multiply(img,Mask_ext)/numpy.sum(Mask_ext)-numpy.multiply(img,Mask_int)/numpy.sum(Mask_int))
            if Value>MaxValue:
                BestDisques=[circles_int[0,i,0],circles_int[0,i,1],circles_ext[0,j,2],circles_int[0,i,2]]
                MaxValue=Value

    print(MaxValue)
    print(BestDisques)
    return BestDisques
