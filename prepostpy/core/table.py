# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: dutzi
"""


import numpy as np
import py_mentat as pm

class Table:
    
    def __init__(self,label,category='time',points=np.zeros((0,2)),
                 *args,**kwargs):
        
        self.label = label
        self.category = category
        self.points = points
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value

    def add_point(self,point):
        self.points = np.vstack((self.points,point))
        
    def add_points(self,points):
        self.points = np.vstack((self.points,points))
        
    def tomentat(self):
        pm.py_send('*new_md_table 1 1')
        pm.py_send('*table_name', self.label)
        pm.py_send('*set_md_table_type 1', self.category)
        for point in self.points:
            p = ' '.join(str(coord) for coord in point)
            pm.py_send('*table_add', p)