# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: dutzi
"""


import numpy as np
import py_mentat as pm

from .boundary import Boundary

class Loadcase:
    
    def __init__(self,label,category='struc:static',
                 time=1,steps=50,multi_criteria=False,boundaries=False,
                 convergence_displacement=False,convergence_force=0.1,
                 *args,**kwargs):
        
        self.label = label
        self.category = category
        self.steps = steps
        self.time = time
        self.multi_criteria = multi_criteria
        self.boundaries = boundaries
        self.convergence_displacement = convergence_displacement
        self.convergence_force = convergence_force
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value
        
    def tomentat(self):
        pm.py_send('*new_loadcase *loadcase_type', self.category)
        pm.py_send('*loadcase_name', self.label)
        
        if self.multi_criteria:
            pm.py_send('*loadcase_option stepping:multicriteria')
            
        if self.steps != 50:
            pm.py_send('*loadcase_value nsteps', str(self.steps))
            
        if self.time != 1:
            pm.py_send('*loadcase_value time', str(self.time))
            
        if self.boundaries is not None:
            pm.py_send('*clear_loadcase_loads')
            for b in self.boundaries:
                if isinstance(b,Boundary):
                    load = b.label
                else:
                    load = b
                pm.py_send('*add_loadcase_loads', load)
                
        if self.convergence_force != 0.1:
            pm.py_send('*loadcase_value force', str(self.convergence_force))
            
        if self.convergence_displacement is not None:
            pm.py_send('*loadcase_option converge:resid_and_disp')
            pm.py_send('*loadcase_value displacement', 
                       str(self.convergence_displacement))