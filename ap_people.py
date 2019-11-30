# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 01:06:28 2019

@author: ariji
"""

import cv2 as cv
import numpy as np
import math 
import os
os.chdir("D:/L_Learning/computer vision/project 2")
import time
#This is a wrapper for openCV basics
import basic_function as bf
#import tensorflow as tf
import tensorflow_human_detection as thd


Frame="people_15"
img = cv.imread("people_detection/"+Frame+".png")
#bf.show_image(img)


#### Method 0 ####
person_cascade = cv.CascadeClassifier(
    os.path.join('haarcascade_fullbody.xml'))
gray_frame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
rects = person_cascade.detectMultiScale(gray_frame)
for (x, y, w, h) in rects:
    cv.rectangle(img, (x,y), (x+w, y+w), (0, 255, 0), 2)
bf.show_image(img)
bf.show_image(gray_frame)
    













### Method1: Haar Cascade for human detection  ###
person_cascade = cv.CascadeClassifier(
    os.path.join('haarcascade_fullbody.xml'))
cap = cv.VideoCapture("test.mp4")
count = 0
while True:
    r, frame = cap.read()
    if r:
        start_time = time.time()
        frame = cv.resize(frame,(640,360)) # Downscale to improve frame rate
        gray_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY) # Haar-cascade classifier needs a grayscale image
        rects = person_cascade.detectMultiScale(gray_frame)
        
        
        end_time = time.time()
        print("Elapsed Time:",end_time-start_time)

            
        for (x, y, w, h) in rects:
            cv.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)
        if len(rects) != 0:
            cv.imwrite("people_detection/people_"+ str(count) +".png", frame)
            count = count + 1

        cv.imshow("preview", frame)   
    k = cv.waitKey(1)


    if k & 0xFF == ord("q"): # Exit condition
        break

cap.release()
cv.destroyAllWindows()

### Histograms of Oriented Gradients for Human Detection (HOG) ###

hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
cap = cv.VideoCapture("test.mp4")
while True:
    r, frame = cap.read()
    if r:
        start_time = time.time()
        frame = cv.resize(frame,(1280, 720)) # Downscale to improve frame rate
        gray_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY) # HOG needs a grayscale image

        rects, weights = hog.detectMultiScale(gray_frame)
        
        # Measure elapsed time for detections
        end_time = time.time()
        print("Elapsed time:", end_time-start_time)
        
        for i, (x, y, w, h) in enumerate(rects):
            if weights[i] < 0.7:
                continue
            cv.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)

        cv.imshow("preview", frame)
    k = cv.waitKey(1)
    if k & 0xFF == ord("q"): # Exit condition
        break
    
cap.release()
cv.destroyAllWindows()

#### modern approach for people detection ####
#Deep convolutional neural network




## The following model_path variable refers to the pretrained model of object detection
## There are 11 compatible models in total
## https://medium.com/@madhawavidanapathirana/real-time-human-detection-in-computer-vision-part-2-c7eda27115c6

#model_path = 'faster_rcnn_inception_v2_coco_2018_01_28/frozen_inference_graph.pb'
model_path = 'faster_rcnn_nas_coco_2018_01_28/frozen_inference_graph.pb'
threshold = 0.7
odapi = thd.DetectorAPI(path_to_ckpt=model_path)
cap = cv.VideoCapture('test.mp4')

while True:
    r, img = cap.read()
    img = cv.resize(img, (1280, 720))
    boxes, scores, classes, num = odapi.processFrame(img)
    # Visualization of the results of a detection.
    for i in range(len(boxes)):
        #Class 1 represents human
        if classes[i] == 1 and scores[i]> threshold:
           box = boxes[i]
           cv.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)
    cv.imshow("Detected people", img) 
    k = cv.waitKey(1)
    if k and 0xFF == ord('q'):
        break  

cap.release()
cv.destroyAllWindows()























