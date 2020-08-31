#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import rospy
import sys
import sqlite3

# Ce programme définit la class codeur et la fonction Acquisition_vitesse
# codeur prend en argument name (str) et pin (int) et définit les fonctions de base
# Acquisition_vitesse crée un codeur et définit son comportement

class codeur():
    def __init__(self,name,pin):
        self.pin=pin
        self.Front=0
        self.dist=0
        self.name=name
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin,GPIO.IN)

        self.value=GPIO.input(self.pin)
        self.debut=time.time()

        # Creation d'une base de donnees
        self.conn=sqlite3.connect('/dev/shm/' + self.name + '_' + str(time.time()) + '.db')
        self.c=self.conn.cursor()
        #c.execute("DROP TABLE CARBOT")
        self.c.execute("CREATE TABLE " + self.name + " (time REAL, dist REAL);")

    def _increment(self):
        self.Front=self.Front+1
    def _get_state(self):
        return GPIO.input(self.pin)
    def _dist(self):
        # Calcul de la distance
        duree=time.time()-self.debut
        self.dist=180*self.Front/20
        self.Front=0
        self.debut=time.time()
    def _save(self):
        # Sauvegarde de la distance parcourue et l'instant de mesure dans la base de données
        self.c.execute("INSERT INTO " + self.name + " (time,dist) VALUES (?,?)",(time.time(), self.dist))
        self.conn.commit()

def Acquisition_vitesse(name,pin):
    # Crée un codeur qui mesure la distance parcourue à 2Hz et la sauvegarde
    Codeur=codeur(name,pin)
    while not rospy.is_shutdown():
        # Incrementer a chaque front
        if Codeur.value!=Codeur._get_state():
            Codeur.value=Codeur._get_state()
            Codeur._increment()
        # Mesure de vitesse 1Hz
        if time.time()-Codeur.debut>0.5:
            Codeur._dist()
            Codeur.debut=time.time()
            Codeur._save()


if __name__=="__main__":
    args=rospy.myargv(argv=sys.argv)
    if len(args)!=3:
        print "Erreur arguments : str int"
        sys.exit(1)
    Acquisition_vitesse(args[1], int(args[2]))
