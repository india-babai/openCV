# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 05:03:19 2019

@author: ariji
"""
import cv2
import numpy as np
import math
import os

os.chdir('D:/L_Learning/computer vision/project 2')

def vid_to_frame(vid_path, folder_path):
    video = cv2.VideoCapture(vid_path)
    count = 0
    while video.isOpened() and count <= 40:
        
        #Setting(fast forwarding) the video at 'count'th milisecond
        video.set(cv2.CAP_PROP_POS_MSEC, count*100)
        
        #Reading the frame at 'count'th sec
        ret, frame = video.read() 
        
        if ret == True:
            
            #Saving the frame
            cv2.imwrite(folder_path + "/frame_v2_" + str(count) + ".png", frame)
            
            #showing the frame
#            cv2.imshow("Original video", frame)
            
            #Option to quit
#            if cv2.waitKey(1) & 0xFF == ord('q'):
#                break            
        else:
            break
        count = count + 1
        
        
    print(f'Total {count} frames saved to ' + folder_path)
    video.release()
    
    cv2.destroyAllWindows()
    #End of vid_to_frame

vid_to_frame('test.mp4', 'vid2frame')
cv2.destroyAllWindows()











