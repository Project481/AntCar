import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread("D:\PFE\Illustrations\Traitement d'image\Samples detection\DB_test9.jpg")
cimg=img
# Convertir en niveaux de gris
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#img = cv2.medianBlur(img,5)


Rmax=int(img.shape[0]/2)
Rmin=int(img.shape[0]/5)

rmax=int(Rmax/4.5)
rmin=int(Rmin/4.5)

circles_ext = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,1,param1=50,param2=30,minRadius=Rmin,maxRadius=Rmax)

circles_ext = np.uint(np.around(circles_ext))



circles_int = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,1,param1=50,param2=30,minRadius=rmin,maxRadius=rmax)

circles_int = np.uint(np.around(circles_int))

Disques=np.zeros((circles_ext.shape[1]*circles_int.shape[1],6))
MaxValue=float('-inf')
BestDisques=[0,0,0,0,0,0]
Value=0

nb_cercle_ext=circles_ext.shape[1]
nb_cercle_int=circles_int.shape[1]
if circles_ext.shape[1]>10:
    nb_cercle_ext=10
    
if circles_int.shape[1]>10:
    nb_cercle_int=10

# Boucle des centres des grands cercles
for i in range(nb_cercle_ext):
    for j in range(nb_cercle_int):
        # Selectionner les pixels à l'exterieur
        Mask_ext=np.ones(img.shape)
        Mask_ext=cv2.circle(Mask_ext, (circles_ext[0,i,0],circles_ext[0,i,1]), circles_ext[0,i,2], 0, -1) 
        # Selectionner les pixels à l'interieur
        Mask_int=np.zeros(img.shape)
        Mask_int=cv2.circle(Mask_int, (circles_ext[0,i,0],circles_ext[0,i,1]), circles_int[0,j,2], 1, -1) 
        
        # Selectionner les pixels de la couronne
        Mask_ring=np.zeros(img.shape)
        Mask_ring=cv2.circle(Mask_ring, (circles_ext[0,i,0],circles_ext[0,i,1]), circles_ext[0,i,2], 1, -1) 
        Mask_ring=cv2.circle(Mask_ring, (circles_ext[0,i,0],circles_ext[0,i,1]), circles_int[0,j,2], 0, -1) 

        Value=np.sum(np.multiply(img,Mask_ring)/np.sum(Mask_ring)-np.multiply(img,Mask_ext)/np.sum(Mask_ext)-np.multiply(img,Mask_int)/np.sum(Mask_int))
        if Value>MaxValue:
            BestDisques=[circles_ext[0,i,0],circles_ext[0,i,1],circles_ext[0,i,2],circles_int[0,j,2]]
            MaxValue=Value
        

# Boucle des centres des petits cercles    
for i in range(nb_cercle_int):
    for j in range(nb_cercle_ext):
        # Selectionner les pixels à l'exterieur
        Mask_ext=np.ones(img.shape)
        Mask_ext=cv2.circle(Mask_ext, (circles_int[0,i,0],circles_int[0,i,1]), circles_ext[0,j,2], 0, -1) 
        # Selectionner les pixels à l'interieur
        Mask_int=np.zeros(img.shape)
        Mask_int=cv2.circle(Mask_int, (circles_int[0,i,0],circles_int[0,i,1]), circles_int[0,i,2], 1, -1) 
        
        # Selectionner les pixels de la couronne
        Mask_ring=np.zeros(img.shape)
        Mask_ring=cv2.circle(Mask_ring, (circles_int[0,i,0],circles_int[0,i,1]), circles_ext[0,j,2], 1, -1) 
        Mask_ring=cv2.circle(Mask_ring, (circles_int[0,i,0],circles_int[0,i,1]), circles_int[0,i,2], 0, -1)  
        
        Value=np.sum(np.multiply(img,Mask_ring)/np.sum(Mask_ring)-np.multiply(img,Mask_ext)/np.sum(Mask_ext)-np.multiply(img,Mask_int)/np.sum(Mask_int))        
        if Value>MaxValue:
            BestDisques=[circles_int[0,i,0],circles_int[0,i,1],circles_ext[0,j,2],circles_int[0,i,2]]
            MaxValue=Value
        
print(MaxValue)
print(BestDisques)

img=cv2.circle(cimg, (BestDisques[0],BestDisques[1]), BestDisques[2], (255,0,0), 5) 
img=cv2.circle(cimg, (BestDisques[0],BestDisques[1]), BestDisques[3], (255,0,0), 5) 

plt.imshow(img,cmap='gray')


x_ext=circles_ext[0,:,0]
y_ext=circles_ext[0,:,1]

x_int=circles_int[0,:,0]
y_int=circles_int[0,:,1]

# =============================================================================
# plt.xlim((0,img.shape[1]))
# plt.ylim((0,img.shape[0]))
# 
# plt.plot(x_ext,y_ext,".r")
# plt.plot(x_int,y_int,".b")
# =============================================================================

x=np.concatenate((x_ext,x_int))
y=np.concatenate((y_ext,y_int))

Centres=[x]
Centres=np.append(Centres,[y],0)




Couronnes=[]





# =============================================================================
# # draw the outer circle
# cv2.circle(cimg,(circles_ext[0,0,0],circles_ext[0,0,1]),circles_ext[0,0,2],(0,255,0),2)
# cv2.circle(cimg,(circles_int[0,0,0],circles_int[0,0,1]),circles_int[0,0,2],(255,0,0),2)
# # draw the center of the circle
# cv2.circle(cimg,(circles_ext[0,0,0],circles_ext[0,0,1]),1,(0,255,0),5)
# cv2.circle(cimg,(circles_int[0,0,0],circles_int[0,0,1]),1,(255,0,0),5)
# plt.imshow(cimg,cmap='gray')
# =============================================================================
