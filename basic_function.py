# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 01:28:19 2019

@author: ariji

Basic functions which are required at every step in
any openCV project are here

"""

import cv2 as cv
import numpy as np
import math 
import os




def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def show_image(mat, winname = ""):
    try:
        cv.imshow(winname, mat)
        print("Image showing on different window!")
        cv.waitKey()
    except Exception as e:
        print(e)
        
#    return(cv.waitKey(k))
#    if cv.waitKey(10) & 0xFF == ord('q'):
#        cv.destroyAllWindows()
    
    
def line_draw(HL_object, main_img, color):
    if HL_object is not None:
         for i in range(0, len(HL_object)):
             rho = HL_object[i][0][0]
             theta = HL_object[i][0][1]
             a = math.cos(theta)
             b = math.sin(theta)
             x0 = a * rho
             y0 = b * rho
             pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
             pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
             cv.line(main_img, pt1, pt2, color, 1, cv.LINE_AA)
    return(main_img)
    

def mask_edge(img, lower_range, upper_range, canny_thres1 = 50, canny_thres2 = 200):
    lower_range = np.array(lower_range, dtype = "uint8")
    upper_range = np.array(upper_range, dtype = "uint8")
    
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    masked = cv.inRange(hsv, lower_range, upper_range)
    dst = cv.Canny(masked, canny_thres1, canny_thres2, 3)
    return([masked, dst])
    

def HLine(img, max_line = 4, starting_thres = 90):
    """
    1. img should be grayscle and Canny applied!
    2. Try to keep max_line value moderate! (2-3)
    3. max_line may not be achieved sometimes because of the discrete incremets of starting_threshold
    """
    HL = cv.HoughLines(img, 1, np.pi/180, starting_thres, None, 0, 0)
    if HL is None:
#        print("It's NONE in HLine")
        return(None)

    if HL is not None:
#        print("It's not NONE in HLine")
        while len(HL) > max_line:
            starting_thres = starting_thres + 3
            HL = cv.HoughLines(img, 1, np.pi/180, starting_thres, None, 0, 0)
            if HL is None:
                HL = cv.HoughLines(img, 1, np.pi/180, starting_thres - 3, None, 0, 0)
                break
                
           
    print("Final threshold: {}".format( starting_thres))
    return({'HoughLine':HL, 'FinalThreshold': starting_thres})
        
    
def distance(point, line):
    """
    THis program helps finding perpendicular distance between 
    a point and a line (openCV "Hough Line Transform detected" line )
    If side_of_origin is True it means, the point is on the same side of the ine where 
    origin is. If side_of_origin is false it's on the other side
    
    """  
    # Getting two points (pt1 and pt2) in cartesian coordinate from Houghline transformed line
    rho, theta = line[0], line[1]     
    a, b = math.cos(theta), math.sin(theta)
    x0, y0 = a * rho, b * rho
    pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
    pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
    
    
    # Equation forming in cartesian coordinate and applying distance formula
    if pt2[0]-pt1[0] != 0:
        slope = (pt2[1]-pt1[1])/(pt2[0]-pt1[0])
        const = slope*pt1[0] - pt1[1]
        dist = abs(point[1] - slope*point[0] + const)/math.sqrt(1**2 + slope**2)
        sign_pt = np.sign(point[1] - slope*point[0] + const)
        sign_origin = np.sign(const)
    else:
        dist = abs(point[0] - pt1[0])
        sign_pt = np.sign(point[0] - pt1[0])
        sign_origin = np.sign(0 - pt1[0])
        
    if sign_pt == sign_origin:
        side_of_origin = True
    else:
        side_of_origin = False
    return([dist, side_of_origin])

def angle(line1 , line2):
    """
    THis program helps finding  angle between 
    two lines (openCV "Hough Line Transform detected" line )
    
    """  
    # Getting two points (pt1 and pt2) in cartesian coordinate from Houghline transformed line
    theta1, theta2 = line1[1], line2[1]     
    m1, m2 = math.tan(theta1), math.tan(theta2)
    
    tan_angle = (m2 - m1)/(1 + m1*m2)
    angle = math.atan(tan_angle)
    return(angle)


