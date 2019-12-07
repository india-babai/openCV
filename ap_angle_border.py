# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 22:06:14 2019

@author: arijit
"""

import cv2 as cv
import numpy as np
import math 
import os
os.chdir("D:/L_Learning/computer vision/project 2/openCV")

#This is a wrapper for openCV basics
import basic_function as bf



#Frame="logo"
#img = cv.imread(Frame+".png")
#bf.show_image(img)


def angle_detection(img, lower_mask = [161, 155, 84], upper_mask = [179, 255, 255], m = 4, st = 80):
    """
    1. Provide appropriate mask ranges for the color of the line that you want to detect
    2. m = max no. of lines to be detected
    3. st = starting_thres that goes into bf.HLine function
    
    """
    img2 = img.copy()
    #Masking and edging red and yellow (Images after applying "cv.Canny" will be used for line drawing)
    color = bf.mask_edge(img2, lower_range = lower_mask, upper_range = upper_mask) 
    #Applying HL
    HL = bf.HLine(color[1], starting_thres = st, max_line = m)
    if HL is None:
        print("No line found, please lower starting_threshold in script")
        return(None)
    
    print("Line found!!")
    
    HL_color = HL['HoughLine']
    #Drawing line
#    color_bgr = cv.cvtColor(color[1], cv.COLOR_GRAY2BGR)
    color_line = bf.line_draw(HL_color, img2, (0, 0, 255))
#    bf.show_image(color_line)
    
    #Angle with lower horizon
    angle = HL_color[:, 0, 1]
    angle_mod = np.where(angle > math.pi/2, 1.5*math.pi - angle, math.pi/2 - angle)    

#    HL_red[:,0,1] = angle_mod
#    avg_r_theta = HL_red.mean(axis = 0) #This should be reported
    return([HL_color, angle_mod, color_line])

#angle_detection(img, m= 1)
