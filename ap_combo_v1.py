s# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 01:43:33 2019

@author: ariji
"""






import cv2 as cv
import numpy as np
import math
import os
os.chdir("D:/L_Learning/computer vision/project 2")
#This is a wrapper for openCV basics
import basic_function as bf
# Border detection codes
import ap_angle_border as ad




#Importing yolo folder
yolo_path =  "D:/L_Learning/computer vision/project 2/yolo"
weights =  "yolov3.weights"     #Weights and configuration file for yolo
config_file  =  "yolov3.cfg"
os.chdir(yolo_path)
import sys
sys.path.insert(1, yolo_path)
import yolo_people_detection as ypd
#--#

import os
os.chdir("D:/L_Learning/computer vision/project 2")





def combo(img):
    
    img2 = img.copy()
    ###Part 1: Border detection and angle detection: refer to 'ap border.py'
    red = ad.angle_detection(img2, m = 1)                            # Red line (default)
    yellow = ad.angle_detection(img2,
                                lower_mask= [20, 100, 100], 
                                upper_mask =  [30, 255, 255], m =1 ) #yellow line
    blue = ad.angle_detection(img2, 
                              lower_mask=[110,50,50], 
                              upper_mask = [130,255,255], m = 1)     # blue line
    
    #---#
    
    
    
    ###Part 2: Tensorflow API people detection, refer to 'tfpeople detection.py'
    img3 = cv.resize(img, None, fx = 0.4, fy = 0.4)
    people_coordinate = ypd.yolo_people(img3, threshold=0.1, showImage= False)
    pedals = people_coordinate[2]           # Returning the pedals only
                                
    #---#
    
    
    
    ###Part 3:  Adjusted coordinates
        # Adjust the coordinate as it was multiplied by 0.4 before yolo
    pedals_adj = [(int(x[0]*2.5), int(x[1]*2.5)) for x in pedals]
        # Checking whether pedals are properly adjusted
    img4 = img.copy() 
    for x in pedals_adj:
        cv.circle(img4, x, 2, (0, 0, 255), 3)
        
    #---#
    
    
    ###Part 4:  Distance from red, blue, yellow line of the pedals
    
    # Saving three different distances(with side_of_origin of course!) for each pedal point
    dist_red, dist_yel, dist_blue = [], [], []
    for points in pedals_adj:
        if red is not None:
            line = red[0][0][0]
            dist_red.append(bf.distance(points, line))
        if red is None:
            dist_red.append(None)

        if yellow is not None:
            line = yellow[0][0][0]
            dist_yel.append(bf.distance(points, line))
        if yellow is  None:
            dist_yel.append(None)

        if blue is not None:
             line = blue[0][0][0]
             dist_blue.append(bf.distance(points, line))
        if blue is None:
            dist_blue.append(None)


    #Removing the audiences

    index_final = []
    for i in range(len(pedals_adj)):
        if dist_red[i][1] == False or dist_yel[i][1] == True:
            pass
        else:
            index_final.append(i)
    
    img5 = img.copy() 
    for x in index_final:
        cv.circle(img5, pedals_adj[x], 2, (0, 0, 255), 3)
    
        
    #---#

    
    ###Part 5:  Mapping pedals and distances on the template rick
    fin_red = [dist_red[i] for i in index_final]
    fin_blue = [dist_blue[i] for i in index_final]
    fin_yel = [dist_yel[i] for i in index_final]
    
    for i in range(len(pedals_adj)):
        
        dist_blue[i][0] = 0.725 * dist_blue[i][0]
        dist_red[i][0] = 2.27*dist_red[i][0]
        dist_yel[i][0] = 2.27*dist_yel[i][0]
       
    
    

    coordinate_final = []
    for i in index_final:
        if dist_blue[i] is not None:
            if dist_red[i] is not None:
                if dist_blue[i][1] == False:
                    x = int(710 + dist_blue[i][0])
                    y = int(621 - dist_red[i][0])
                    coordinate_final.append((x,y))
                else:
                    x = int(710 - dist_blue[i][0])
                    y = int(621 - dist_red[i][0])
                    coordinate_final.append((x,y))
            else:
                if dist_yel[i] is not None:
                    if dist_blue[i][1] == False:
                        x = int(710 + dist_blue[i][0])
                        y = int(dist_yel[i][0])
                        coordinate_final.append((x,y))
                    else:
                        x = int(710 - dist_blue[i][0])
                        y = int(dist_yel[i][0])
                        coordinate_final.append((x,y)) 
        else:
            coordinate_final.append(None)
     
    template2 = template.copy()
#    bf.show_image(template2)

    for w in coordinate_final:
        if w is not None:
            cv.circle(template2, w, 40, (0, 255, 0), 2)
#    bf.show_image(template2)
    return(template2)


frame="rink template"
template = cv.imread(frame+".png")
bf.show_image(template)


frame="frame_v2_3"
img = cv.imread("vid2frame/"+frame+".png")
#bf.show_image(img)
l = combo(img)
bf.show_image(l)

for i in  range(41):
    img = cv.imread("vid2frame/"+ "frame_v2_" + str(i) + ".png")
    try:
        final_image = combo(img)
        cv.imwrite("vid2frame" + "/final" + str(i) + ".png", final_image)
    except:
        pass
    print(i)
           
#                #showing the frame
#    cv.imshow("Final", final_image)
#            
#            #Option to quit
#    if cv.waitKey(1) & 0xFF == ord('q'):
#        break      
cv.destroyAllWindows()





