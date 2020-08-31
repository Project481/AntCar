#!/usr/bin/env python3

import time
import board
import busio
import adafruit_lsm303dlh_mag
import adafruit_lsm303_accel
import sqlite3

# Définition de la classe Compas et de la fonction Acquisition_Compas
# Compas permet de définir les fonctions principales du magnétomètre et de l'accéléromètre
# Acquisition_Compas crée une instance Compas et lance une acquisition à 10Hz
class Compas():

    def __init__(self,path):
        self.i2c=busio.I2C(board.SCL,board.SDA)
        self.accel=adafruit_lsm303_accel.LSM303_Accel(self.i2c)
        self.mag=adafruit_lsm303dlh_mag.LSM303DLH_Mag(self.i2c)

        # Creation d'une base de donnees
        self.conn=sqlite3.connect(path + 'Compas_' + str(time.time()) + '.db')
        self.c=self.conn.cursor()
        #c.execute("DROP TABLE CARBOT")
        self.c.execute('''CREATE TABLE Compas (time REAL, acc_x REAL, acc_y REAL,acc_z REAL,mag_x REAL,mag_y REAL,mag_z REAL);''')


    def _Add(self):
        # Insertion des donnees dans la base de donnees
        acc_x,acc_y,acc_z=self.accel.acceleration[0],self.accel.acceleration[1],self.accel.acceleration[2]
        mag_x,mag_y,mag_z=self.mag.magnetic[0],self.mag.magnetic[1],self.mag.magnetic[2]
        self.c.execute("INSERT INTO Compas (time, acc_x,acc_y,acc_z,mag_x,mag_y,mag_z) VALUES (?,?,?,?,?,?,?)",(time.time(), acc_x,acc_y,acc_z,mag_x,mag_y,mag_z))
        self.conn.commit()
def Acquisition_Compas(directory):
    MonCompas=Compas(directory)
    while 1:
        time.sleep(0.1)
        MonCompas._Add()

if __name__=="__main__":
    Acquisition_Compas('/dev/shm/')
