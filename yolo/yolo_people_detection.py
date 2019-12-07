# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 02:36:24 2019

@author: ariji
"""



#####---- For running this file from this script , uncomment the necessary libraries ----- ####

import cv2 as cv # computer vision library
import numpy as np
import os
##
import sys
sys.path.insert(1, "D:/L_Learning/computer vision/project 2")
import basic_function as bf

yolo_path =  "D:/L_Learning/computer vision/project 2/openCV/yolo/"
weights =  "yolov3.weights"     #Weights and configuration file for yolo
config_file  =  "yolov3.cfg"
os.chdir(yolo_path)



###load YOLO
net = cv.dnn.readNet(weights, config_file)

classe = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines() ]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size = (len(classes), 3))

#Loading image
#frame = "frame2"
#img = cv.imread(frame+".png")
#img = cv.resize(img, None, fx = 0.4, fy = 0.4)
#height, width, channel = img.shape
#bf.show_image(img)



def yolo_people(img, threshold = 0.5, showImage = True, saveImage = False, newImageName = ""):    
    
    ##### Detecting objects: Deep neural network #####
    img = img.copy()
    height, width, channel = img.shape
    
#    The Blob size can be changed to one of the three (320, 320), (609, 609), (416, 416)
    blob = cv.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop= False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    #Showing information on screen
    class_ids = []
    confidences = []
    boxes = []
    diag, pedal = [], []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            # Setting this class_id == 0 to detect person only
            if confidence > threshold and class_id == 0:
                
                #Person detected: prooviding the center, height and width
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)
                
                #Rectangle coordinates
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x, y, w, h])
                
                #Note: Diagonal and pedal midpoint coordinates are in openCV coordinate system
                diag_intersect = (center_x, center_y)
                pedal_midpoint =  (center_x, int(center_y + h/2))
#                print(diag_intersect, pedal_midpoint)
                diag.append(diag_intersect)
                pedal.append(pedal_midpoint)
                
                confidences.append(float(confidence))
                class_ids.append(class_id)
                    
    indexes = cv.dnn.NMSBoxes(boxes, confidences, threshold, 0.4)
    
    #Drawing the image
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            color = colors[i]
            cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv.circle(img, (int(x + w/2), int(y + h/2)), 2, (0, 0, 255), 3)
            cv.circle(img, (int(x + w/2), y+h), 2, (0, 0, 255), 3)
    
    if showImage:
        bf.show_image(img)
    if saveImage:
        cv.imwrite(newImageName, img)
    return([boxes, diag, pedal, img])
    

##Loading image
#frame = "frame1"
#img = cv.imread(frame+".png")
#img = cv.resize(img, (416, 416))
#img = cv.resize(img, None, fx = 0.4, fy = 0.4)
##img = cv.resize(img, (1280, 720))
#height, width, channel = img.shape
##bf.show_image(img)
#yolo_people(img, threshold=0.1)



   #### Saving detected frames
#def a(string, x):
#    if string in x:
#        return(x)
#list_of_frames = [a("png", x) for x in os.listdir()]
##
#for i in range(len(list_of_frames)):
#    if list_of_frames[i] is not None:
#        img = cv.imread(list_of_frames[i])
#        img = cv.resize(img, None, fx = 0.4, fy = 0.4)
#        yolo_people(img, threshold=0.1, showImage= False, saveImage= True, newImageName = "yolod_"+list_of_frames[i])





    
