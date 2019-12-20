# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 00:26:49 2019

@author: ariji

This script won't be run standalone! It is referred to ap_combo_v1.py

"""


if position == "L":
        for i in index_final:
            if blue is not None:
                if red is not None:
                    if dist_blue[i][1] == False:
                        x = int(355 + dist_blue[i][0])
                        y = int(621 - dist_red[i][0])
                        coordinate_final.append((x,y))
                    else:
                        x = int(355 - dist_blue[i][0])
                        y = int(621 - dist_red[i][0])
                        coordinate_final.append((x,y))
                else:
                    if yellow is not None:
                        if dist_blue[i][1] == False:
                            x = int(355 + dist_blue[i][0])
                            y = int(dist_yel[i][0])
                            coordinate_final.append((x,y))
                        else:
                            x = int(355 - dist_blue[i][0])
                            y = int(dist_yel[i][0])
                            coordinate_final.append((x,y)) 
        else:
            if red is not None:
                    x = int(1065 - 0.5*dist_yel[i][0]/abs(math.sin(ang_yel_red)))
                    y = int(621 - dist_red[i][0]* 621/(max(fin_red)[0] + 30))
                    coordinate_final.append((x,y)) 
                    
                    
if position == "R":
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










