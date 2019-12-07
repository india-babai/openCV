# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 00:40:09 2019

@author: ariji

testing.py is for doing rough work! It doesn't have any maintanable/reproducible code

"""



import cv2 as cv
import numpy as np
import math
import os
os.chdir("D:/L_Learning/computer vision/project 2/openCV")
#This is a wrapper for openCV basics
import basic_function as bf
# Border detection codes
import ap_angle_border as ad


frame_no = 25
img = cv.imread("vid2frame/"+ "frame_v2_" + str(frame_no) + ".png")
bf.show_image(img)

lower_mask=[110,50,50] 
upper_mask = [130,255,255]
b = bf.mask_edge(img, lower_range = lower_mask, upper_range=upper_mask)
bf.show_image(b[1]) 




lower_mask= [20, 100, 100]
upper_mask =  [30, 255, 255]
y = bf.mask_edge(img, lower_range = lower_mask, upper_range=upper_mask)
bf.show_image(y[1]) 





lower_mask = [161, 155, 84]
upper_mask = [179, 255, 255]
r = bf.mask_edge(img, lower_range = lower_mask, upper_range=upper_mask)
bf.show_image(r[1]) 

f = b[1]+y[1]+r[1]

bf.show_image(f)

rl = red[0][0][0]
yl = yellow[0][0][0]
bl = blue[0][0][0]

bf.angle(rl, yl)

  











































