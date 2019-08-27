# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:08:52 2019

@author: dutzi
"""

import py_mentat as pm

class ChangeClass:
    
    def __init__(self):
        pass
    
    def toquadratic(self,elements):
        pm.py_send('*change_elements_quadratic',elements)
        
    def tolinear(self,elements):
        pm.py_send('*change_elements_linear',elements)
        
    def toclass(self,new_class,elements):
        pm.py_send('*set_change_class', new_class.lower().replace(' ',''))
        pm.py_send('*change_elements_class', elements)