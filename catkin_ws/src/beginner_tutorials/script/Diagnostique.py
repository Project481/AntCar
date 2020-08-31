#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import time

class image_converter:

  def __init__(self):

    self.image_sub = rospy.Subscriber("/raspicam_node/image_raw",Image,self.callback)
    self.compt=0
    self.debut=time.time()

  def callback(self,data):
     self.compt=self.compt+1
     print("FPS : ",self.compt/(time.time()-self.debut))
     print("elapsed : ",(time.time()-self.debut))
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
