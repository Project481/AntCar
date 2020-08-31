# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 17:31:25 2020

@author: Florentin
"""

import skimage.io as io
import matplotlib.pyplot as plt
import numpy
import skimage.morphology
import skimage.feature
import colorsys
import scipy.signal
from scipy import ndimage
from skimage.transform import hough_circle, hough_circle_peaks
import time
from skimage import data, color
from skimage.draw import circle_perimeter
import cv2

def HoughTransform(image):

    def gaussian_kernel(size, sigma=1):
        size = int(size) // 2
        x, y = numpy.mgrid[-size:size+1, -size:size+1]
        normal = 1 / (2.0 * numpy.pi * sigma**2)
        g =  numpy.exp(-((x**2 + y**2) / (2.0*sigma**2))) * normal
        return g

    f_blur=scipy.signal.convolve2d(image,gaussian_kernel(5,5),mode='same',boundary='symm')

    def sobel_filters(img):
        Kx = numpy.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], numpy.float32)
        Ky = numpy.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], numpy.float32)

        Ix = ndimage.filters.convolve(img, Kx)
        Iy = ndimage.filters.convolve(img, Ky)

        G = numpy.hypot(Ix, Iy)
        G = G / G.max() * 255
        theta = numpy.arctan2(Iy, Ix)

        return (G, theta)


    [G,theta]=sobel_filters(f_blur)


    def non_max_suppression(img, D):
        M, N = img.shape
        Z = numpy.zeros((M,N), dtype=numpy.int32)
        angle = D * 180. / numpy.pi
        angle[angle < 0] += 180


        for i in range(1,M-1):
            for j in range(1,N-1):
                try:
                    q = 255
                    r = 255

                   #angle 0
                    if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] <= 180):
                        q = img[i, j+1]
                        r = img[i, j-1]
                    #angle 45
                    elif (22.5 <= angle[i,j] < 67.5):
                        q = img[i+1, j-1]
                        r = img[i-1, j+1]
                    #angle 90
                    elif (67.5 <= angle[i,j] < 112.5):
                        q = img[i+1, j]
                        r = img[i-1, j]
                    #angle 135
                    elif (112.5 <= angle[i,j] < 157.5):
                        q = img[i-1, j-1]
                        r = img[i+1, j+1]

                    if (img[i,j] >= q) and (img[i,j] >= r):
                        Z[i,j] = img[i,j]
                    else:
                        Z[i,j] = 0

                except IndexError as e:
                    pass

        return Z

    img_fin=non_max_suppression(G,theta)

    def threshold(img, lowThresholdRatio=0.05, highThresholdRatio=0.09):

        highThreshold = img.max() * highThresholdRatio;
        lowThreshold = highThreshold * lowThresholdRatio;

        M, N = img.shape
        res = numpy.zeros((M,N), dtype=numpy.int32)

        weak = numpy.int32(25)
        strong = numpy.int32(255)

        strong_i, strong_j = numpy.where(img >= highThreshold)
        zeros_i, zeros_j = numpy.where(img < lowThreshold)

        weak_i, weak_j = numpy.where((img <= highThreshold) & (img >= lowThreshold))

        res[strong_i, strong_j] = strong
        res[weak_i, weak_j] = weak

        return (res, weak, strong)

    [res,weak,strong]=threshold(img_fin)

    # =============================================================================
    # def hysteresis(img, weak, strong=255):
    #     M, N = img.shape
    #     for i in range(1, M-1):
    #         for j in range(1, N-1):
    #             if (img[i,j] == weak):
    #                 try:
    #                     if ((img[i+1, j-1] == strong) or (img[i+1, j] == strong) or (img[i+1, j+1] == strong)
    #                         or (img[i, j-1] == strong) or (img[i, j+1] == strong)
    #                         or (img[i-1, j-1] == strong) or (img[i-1, j] == strong) or (img[i-1, j+1] == strong)):
    #                         img[i, j] = strong
    #                     else:
    #                         img[i, j] = 0
    #                 except IndexError as e:
    #                     pass
    #     return img
    #
    # img_hys=hysteresis(res,weak)
    # =============================================================================



    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
    image = color.gray2rgb(image)


    hough_radii=numpy.arange(35,45,1)
    hough_res = hough_circle(res, hough_radii)

    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                               total_num_peaks=1)


    cx,cy,r=cx[0],cy[0],radii[0]
    cv2.circle(image,(cx, cy),radii, (255,0,0), 5)


    hough_radii=numpy.arange(180,200,1)
    hough_res = hough_circle(res, hough_radii)

    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                               total_num_peaks=1)


    Cx,Cy,R=cx[0],cy[0],radii[0]
    cv2.circle(image,(Cx, Cy),R, (255,0,0), 5)

    plt.imshow(image)
    return(image,cx,cy,r,Cx,Cy,R)