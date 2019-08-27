# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:08:52 2019

@author: dutzi
"""

import numpy as np
import py_mentat as pm

class Move:
    
    def __init__(self):
        self.centroid = np.array([0,0,0])
        self.scale_factors = np.array([1,1,1])
        self.rotation_angles = np.array([0,0,0])
        self.translations = np.array([0,0,0])
        self.formulas = ['x','y','z']
        
    def move(self,objects='Model'):
        xi = ['x','y','z']
        for x,v in zip(xi,self.centroid):
            pm.py_send('*set_move_centroid %s %s' % (x, str(v)))
        for x,v in zip(xi,self.scale_factors):
            pm.py_send('*set_move_scale_factor %s %s' % (x, str(v)))
        for x,v in zip(xi,self.rotation_angles):
            pm.py_send('*set_move_rotation %s %s' % (x, str(v)))
        for x,v in zip(xi,self.translations):
            pm.py_send('*set_move_translation %s %s' % (x, str(v)))
        for x,v in zip(xi,self.formulas):
            pm.py_send('*set_move_formula %s %s' % (x, str(v)))
                
        move_command = '*move_'+objects.lower()
        if objects.lower() != 'model':
            move_command = move_command + ' all_existing'
        pm.py_send(move_command) 