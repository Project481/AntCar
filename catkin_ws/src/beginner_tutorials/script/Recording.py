#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from Fct_unwrapping import LookUpTable
import scipy
import math
import time
import numpy
from datetime import datetime
import os
from HoughDetection import DetectionCouronne

class image_converter:

  def __init__(self):

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/raspicam_node/image_raw",Image,self.callback)
    self.Initialisation=0

    # Paramètres pour le rééchantillonnage des images
    resolution=1
    self.final_size1=(int(360/resolution),int(82/resolution))
    resolution=5
    self.final_size5=(int(360/resolution),int(82/resolution))
    resolution=10
    self.final_size10=(int(360/resolution),int(82/resolution))

    # Création des répertoires de sauvegarde dans /dev/shm/ (RAM)
    maintenant=datetime.now()
    self.folder='Recording ' + str(maintenant.hour) + '-'+ str(maintenant.minute)+ '-'+ str(maintenant.second)+ ' '+ str(maintenant.day)+ '.' + str(maintenant.month)+ '.' + str(maintenant.year)
    os.mkdir('/dev/shm/' + self.folder)
    os.mkdir('/dev/shm/' + self.folder + '/Originale')
    os.mkdir('/dev/shm/' + self.folder + '/Panorama')

  def callback(self,data):
    # --- Acquisition ---
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "mono8")
    except CvBridgeError as e:
      print(e)

    # --- Initialisation realisee une seule fois ---
    if not(self.Initialisation):

        # Detection de la couronne
        Couronne=DetectionCouronne(cv_image)

        # Enregistrement des caracteristiques de la couronne
        self.Cx=float(Couronne[0])
        self.Cy=float(Couronne[1])
        self.Re=float(Couronne[2])
        self.Ri=float(Couronne[3])

        # Enregistrer l'image qui a servi a detecter les cercles
        cv2.circle(cv_image, (int(self.Cx),int(self.Cy)), int(self.Re), 255)
        cv2.circle(cv_image, (int(self.Cx),int(self.Cy)), int(self.Ri), 255)
        cv2.imwrite('/dev/shm/' + self.folder + '/Hough.tif',cv_image)

        # Creation de la table de la table de correspondance entre l'image originale et le panorama
        self.IndX,self.IndY=LookUpTable(self.Cx,self.Cy,self.Re,self.Ri)

        self.Initialisation=1

    # --- Unwraping ---
    self.Panorama=cv_image[self.IndY,self.IndX]

    # --- Reechantillonnage ---
    # L'image est rééchantillonnee pour trois résolutions
    self.resampled1=cv2.resize(self.Panorama,self.final_size1,interpolation = cv2.INTER_NEAREST)
    self.resampled5=cv2.resize(self.Panorama,self.final_size5,interpolation = cv2.INTER_NEAREST)
    self.resampled10=cv2.resize(self.Panorama,self.final_size10,interpolation = cv2.INTER_NEAREST)

    # --- Visualisation ---
    # Décommenter ci-dessous dans les phases de debugging pour visualiser l'images sur un écran
    # /!\ commenter si la raspberry n'est pas connectee a un ecran !
    cv2.circle(cv_image, (int(self.Cx),int(self.Cy)), int(self.Re), 255)
    cv2.circle(cv_image, (int(self.Cx),int(self.Cy)), int(self.Ri), 255)
    #cv2.imshow("Image window", cv_image)


    # --- Enregistrement sur la RAM ---
    # Enregistrement des images (Non deroulee, reechantillonnees) sur la RAM
    cv2.imwrite('/dev/shm/' + self.folder + '/Originale/Originale_' + str(time.time()) + '.tif',cv_image)
    cv2.imwrite('/dev/shm/' + self.folder + '/Panorama/image_1_' + str(time.time()) + '.tif',self.resampled1)
    cv2.imwrite('/dev/shm/' + self.folder + '/Panorama/image_5_' + str(time.time()) + '.tif',self.resampled5)
    cv2.imwrite('/dev/shm/' + self.folder + '/Panorama/image_10_' + str(time.time()) + '.tif',self.resampled10)
    cv2.waitKey(3)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)

  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
