#!/usr/bin/python
import rospy
import RPi.GPIO as GPIO
# Ce programme permet de mettre la pin 17 à l'état haut et 27 à l'état bas pour que les deux roues du robot tournent en marche avant
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17,1)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27,0)
