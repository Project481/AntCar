#!/usr/bin/python

import rospy
import time


def init():
    self.pub = rospy.Publisher('/servos_absolute', ServoArray,queue_size=100)
    rospy.init_node('ControleMoteur', anonymous=True)



class Moteur:
    # Initialiser un moteur et le message a envoyer
    def __init__(self,pwm1,pwm2):

        
        rospy.on_shutdown(self.arret)
        self.rate = rospy.Rate(20) # 10hz
        self.msg=ServoArray()
        self.Servo1=Servo()
        self.Servo2=Servo()
        self.Servo1.servo=pwm1
        self.Servo1.value=0
        self.Servo2.servo=pwm2
        self.Servo2.value=0
        self.msg.servos=[self.Servo1, self.Servo2]
    # Procedure d'arret
    def arret(self):
        print "STOP !"
        self.Servo1.value=0
        self.Servo2.value=0
        self.msg.servos=[self.Servo1, self.Servo2]
        rospy.loginfo(self.msg)
        self.pub.publish(self.msg)
    # Publication du message sur le topic
    def Pub_msg(self,value):
        self.Servo1.value=value
        self.Servo2.value=value
        self.msg.servos=[self.Servo1, self.Servo2]
        self.debut=time.time()
        while not rospy.is_shutdown():

            if time.time()-self.debut>20:
                rospy.signal_shutdown("We are done here!")
            #rospy.loginfo(self.msg)
            self.pub.publish(self.msg)



if __name__ == '__main__':
    try:

        time.sleep(60)
        Moteur=Moteur(15,16)
        Moteur.Pub_msg(4000)

    except rospy.ROSInterruptException:
        pass
