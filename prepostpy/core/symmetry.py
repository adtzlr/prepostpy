# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:08:52 2019

@author: dutzi
"""

import numpy as np
import py_mentat as pm

class Symmetry:
    
    def __init__(self):
        self.point = np.array([0,0,0])
        self.normal = np.array([1,0,0])
        
    def symmetry(self,objects='Model',point=[0,0,0],normal=[1,0,0]):
        self.point = point
        self.normal = normal
        
        if objects.lower() == 'combined':
            pm.py_send("*symmetry_reset")
        
        x,y,z = self.point
        pm.py_send("*set_symmetry_point %f %f %f" % (x,y,z))
        
        nx,ny,nz = self.normal
        pm.py_send("*set_symmetry_normal %f %f %f" % (nx,ny,nz))
                
        if objects.lower() == 'model':
            objects = 'combined'
            
        move_command = '*symmetry_'+objects.lower()
        move_command = move_command + ' all_existing'
        pm.py_send(move_command)