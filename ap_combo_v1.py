# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 01:43:33 2019

@author: ariji
"""





# Importing bassic necessary packages
import cv2 as cv
import numpy as np
import math
from datetime import date
import os
os.chdir("D:/L_Learning/computer vision/project 2/openCV")
#This is a wrapper for openCV basics
import basic_function as bf
# Border detection codes
import ap_angle_border as ad
#--#



#Importing yolo folder
yolo_path =  "D:/L_Learning/computer vision/project 2/openCV/yolo"
os.chdir(yolo_path)
import sys
sys.path.insert(1, yolo_path)
import yolo_people_detection as ypd
#--#

#Changing the working directory back to what was earlier
import os
os.chdir("D:/L_Learning/computer vision/project 2/openCV")
#--#



frame_no = 58
img = cv.imread("vid2frame/2019-12-20/"+ "frame_v2_" + str(frame_no) + ".png")
bf.show_image(img)
    



def combo(img):
    
    ###Part 1: Tensorflow API people detection, refer to 'tfpeople detection.py'
    img2 = cv.resize(img, None, fx = 0.4, fy = 0.4)
    people_coordinate = ypd.yolo_people(img2, threshold=0.1, showImage= False)
    pedals = people_coordinate[2]           # Returning the pedals only
                                
    #---#
    
    
    ###Part 2:  Adjusted coordinates
        # Adjust the coordinate as it was multiplied by 0.4 before yolo
    pedals_adj = [(int(x[0]*2.5), int(x[1]*2.5)) for x in pedals]
        # Checking whether pedals are properly adjusted
#    img3 = img.copy() 
#    for x in pedals_adj:
#        cv.circle(img3, x, 2, (0, 0, 255), 3)
#    bf.show_image(img3)    
    #---#
    
    
    
    
    ###Part 3: Border detection and angle detection: refer to 'ap border.py'
    img4 = img.copy()
    red = ad.angle_detection(img4, m = 1)                            # Red line (default)
    yellow = ad.angle_detection(img4,
                                lower_mask= [20, 100, 100], 
                                upper_mask =  [30, 255, 255], m = 1) #yellow line
    blue = ad.angle_detection(img4, 
                              lower_mask=[110,50,50], 
                              upper_mask = [130,255,255], m = 1, st = 65)     # blue line  
    #---#
    
    
    
    ###Part 4: Angle between the borders
    angle = []
    for x in [(blue, red), (red, yellow), (yellow, blue)]:
        if None not in x:
            a =  bf.angle(line1= x[0][0][0][0], line2 = x[1][0][0][0])
            angle.append(a)
        else:
            angle.append(None)
    
    ang_blue_red, ang_yel_red, ang_yel_blue = angle[0], angle[1], angle[2]

            
    #---#
    
    
    ###Part 5:  Perpendicular distance from red, blue, yellow line of the pedals
    
    # Saving three different distances(with side_of_origin of course!) for each pedal point
    dist_red, dist_yel, dist_blue = [], [], []
    for points in pedals_adj:
        temp = []
        for x in (red, yellow, blue):
            if x is not None:
                temp.append(bf.distance(points, x[0][0][0]))
            else:
                temp.append((None, None))
        dist_red.append(temp[0])
        dist_yel.append(temp[1])
        dist_blue.append(temp[2])
        
#    Deciding if the upper yellow or the side yellow is captured (Noot doen yet, To be added)
    
        
    # Removing the audiences (Not final yet: Need to add some filters based on yellow line, if required)
    # It has to be automated whether the upper yellow or,
    #   the right hand side yellow border has been captured in yel
    
    index_final = []
    for i in range(len(pedals_adj)):
        if red is not None:
            if dist_red[i][1] == True or dist_yel[i][1] == False:
                index_final.append(i)
            else:
                pass
        else:
            if dist_yel[i][1] == False:
                index_final.append(i)
                
    #Checking if the audiences are really removed
#    img5 = img.copy()
#    for x in index_final:
#        cv.circle(img5, pedals_adj[x], 2, (0, 0, 255), 3)
#        cv.putText(img5,str(x), pedals_adj[x], cv.FONT_HERSHEY_SIMPLEX, 0.8, 255, 2)
#    bf.show_image(img5)
    
    #---#

    
    ###Part 6:  Mapping pedals and distances on the template rink
    # This scaling is very inportant part! 
    # As ultimately the coordinates depend on how accurate the scaling is.
    
    fin_red = [dist_red[i] for i in index_final]
    fin_blue = [dist_blue[i] for i in index_final]
    fin_yel = [dist_yel[i] for i in index_final]
    
    for i in range(len(pedals_adj)):
        if red is not None:
            dist_red[i][0] = 1*dist_red[i][0]
        if yellow is not None:
            dist_yel[i][0] = 0.725*dist_yel[i][0]
        if blue is not None:
            dist_blue[i][0] = 0.725 * dist_blue[i][0]
            


#Scaling
#        dist_blue[i][0] = 0.725 * dist_blue[i][0]
#        dist_red[i][0] = 2.27*dist_red[i][0]
#        dist_yel[i][0] = 2.27*dist_yel[i][0]
       
    #---#
        
    ang_hor = red[1][0]
    
    
    ###Part 7:  PLacing the players in based on scaled final coordinates

    coordinate_final = []
    for i in index_final:
        if blue is not None:
            if red is not None:
                if dist_blue[i][1] == False:
                    x = int(710 + dist_blue[i][0])
                    y = int(621 - dist_red[i][0])
                    coordinate_final.append((x,y))
                else:
                    x = int(710 - dist_blue[i][0])
                    y = int(621 - dist_red[i][0])
                    coordinate_final.append((x,y))
            else:
                if yellow is not None:
                    if dist_blue[i][1] == False:
                        x = int(710 + dist_blue[i][0])
                        y = int(dist_yel[i][0])
                        coordinate_final.append((x,y))
                    else:
                        x = int(710 - dist_blue[i][0])
                        y = int(dist_yel[i][0])
                        coordinate_final.append((x,y)) 
        else:
            if red is not None:
                    x = int(1065 - 0.5*dist_yel[i][0]/abs(math.sin(ang_yel_red)))
                    y = int(621 - dist_red[i][0]* 621/(max(fin_red)[0] + 30))
                    coordinate_final.append((x,y))        

    #---#
    
    
    ###Part 8:  Drawing of final image that is to be returned 
    template2 = template.copy()
    for w, i in zip(coordinate_final, index_final):
        if w is not None:
            cv.circle(template2, w, 15, (0, 255, 0), 2)
            cv.putText(template2, str(i), w, cv.FONT_HERSHEY_SIMPLEX, 0.8, 255, 2)
#    bf.show_image(template2)
    temp3 = cv.resize(template2, (640, 360))
    vis = np.concatenate((img5, temp3), axis = 0)
    bf.show_image(vis)
    
    #---#
    return([template2, vis])





frame="rink template"
template = cv.imread(frame+".png")
bf.show_image(template)


frame_no = 18
img = cv.imread("vid2frame/"+ "frame_v2_" + str(frame_no) + ".png")

bf.show_image(img)
l = combo(img)
bf.show_image(l)


today = str(date.today())
bf.createFolder("vid2frame/"+today)
for i in  range(19, 26):
    img = cv.imread("vid2frame/"+ "frame_v2_" + str(i) + ".png")
    try:
        final_image = combo(img)
        cv.imwrite("vid2frame/" + today +"/comb_" + str(i) + ".png", final_image[1])
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





