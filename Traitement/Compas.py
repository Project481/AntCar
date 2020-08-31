# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 09:33:59 2020

@author: Florentin
"""



import numpy as np
from matplotlib import pyplot as plt
import sqlite3

conn=sqlite3.connect("D:\PFE\Test2905\Ligne droite\Lineaire.db")
cur=conn.cursor()
# Creation d'une requete
req="SELECT * FROM CARBOT"
cursor = cur.execute(req)
# Stock toutes les données dans une liste de listes
alist = cursor.fetchall()
# Conversion de alist en array
data1 = np.array(alist)

plt.plot(data1[:,0])

