# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 10:47:29 2020

@author: Florentin
"""

import cv2
import numpy as np
import itertools
import math
import matplotlib.pyplot as plt

def daugman(center: 'Tuple[int, int]', start_r: int,end_r: int,
            gray_img: 'np.array') -> 'Tuple[float, Tuple[Tuple[int, int], int]]':
    """ Function will find maximal intense radius for given center
        :param center:  center coordinates ``(x, y)``
        :param start_r: start radius in pixels
        :param gray_img: grayscale picture
        .. attention::
            Input grayscale image should be a square, not a rectangle
        :return: (intensity_value, ((xc, yc), radius))
    """
    # get separate coordinates
    x, y = center
    # get img dimensions
    h, w = gray_img.shape
    # define some other vars
    tmp = []
    mask = np.zeros_like(gray_img)
    # for every radius in range
    # we are presuming that iris will be no bigger than 1/3 of picture
    for r in range(start_r, end_r):
        # draw circle on mask
        cv2.circle(mask, center, r, 1, -1)
        cv2.circle(mask, center, int(r/4.44), 0, -1)
        # get pixel from original image
        #radii = np.logical_and(gray_img >30, mask)  # it is faster than np or cv2
        radii=gray_img*mask-gray_img
        #normalize np.add.reduce faster than .sum()
        tmp.append(np.add.reduce(radii[radii > 0]) / (math.pi * r*r*(1-1/4.44)))
        # refresh mask
        mask.fill(0)

    # calculate delta of radius intensitiveness
    tmp_np = np.array(tmp, dtype=np.float32)
    tmp_np = tmp_np[1:] - tmp_np[:-1]  # x5 faster than np.diff()
    # aply gaussian filter
    #tmp_np = abs(cv2.GaussianBlur(tmp_np[:-1], (1, 5), 0))
    # get maximum value
    idx = np.argmax(tmp_np)
    # return value, center coords, radius
    val = tmp[idx]
    return val, (center, idx + start_r)


def find_iris(gray: 'np.ndarray',
              start_r: int,end_r: int,pos_x:int,pos_y:int) -> 'Tuple[Tuple[int, int], int]':
    """ Function will apply :mod:`daugman()` on every pixel
        in calculated image slice. Basically, we are calculating
        where lies set of valid circle centers.
        Selection of image slice guarantees that every
        radius will be drawn in image borders.
        :param gray: graysacale square image
        :param start_r: initial radius
        :return: radius with biggest intensiveness delta on image as ``((xc, yc), radius)``
    """
    _, s = gray.shape
    # reduce step for better accuracy
    # 's/3' is the maximum radius of a daugman() search
    a = range( int(pos_x-15), int(pos_x+15), 1)
    b = range( int(pos_y-15), int(pos_y+15), 1)
    
    all_points = itertools.product(a, b)
    

    values = []
    coords = []

    for p in all_points:
        tmp = daugman(p, start_r,end_r, gray)
        if tmp is not None:
            val, circle = tmp
            values.append(val)
            coords.append(circle)

    # return the radius with biggest intensiveness delta on image
    # ((xc, yc), radius)
    # x10 faster than coords[np.argmax(values)]
    return coords[values.index(max(values))]