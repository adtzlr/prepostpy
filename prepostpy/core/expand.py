# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:08:52 2019

@author: dutzi
"""

import numpy as np
import py_mentat as pm
#from .curve import Curve
from .element import Element

class Expand:
    
    def __init__(self):
        self.category = 'Elements'
        self.centroid = np.array([0,0,0])
        self.scale_factors = np.array([1,1,1])
        self.rotation_angles = np.array([0,0,0])
        self.translations = np.array([0,0,0])
        self.repetitions = 0
        
    def expand(self,elements,
               centroid = np.array([0,0,0]),
               scale_factors = np.array([1,1,1]),
               rotation_angles = np.array([0,0,0]),
               translations = np.array([0,0,0]),
               repetitions = 0):
        
        self.centroid = centroid
        self.scale_factors = scale_factors
        self.rotation_angles = rotation_angles
        self.translations = translations
        self.repetitions = repetitions
        
        xi = ['x','y','z']
        for x,v in zip(xi,self.centroid):
            pm.py_send('*set_expand_centroid %s %s' % (x, str(v)))
        for x,v in zip(xi,self.scale_factors):
            pm.py_send('*set_expand_scale_factors %s %s' % (x, str(v)))
        for x,v in zip(xi,self.rotation_angles):
            pm.py_send('*set_expand_rotation %s %s' % (x, str(v)))
        for x,v in zip(xi,self.translations):
            pm.py_send('*set_expand_translation %s %s' % (x, str(v)))
        pm.py_send('*set_expand_repetitions', str(self.repetitions)) 
        
        if type(elements)!=str:
            if isinstance(elements[0],Element):
                element_list = ' '.join(str(x.mentat_id) for x in elements)
            else:
                element_list = ' '.join(str(x) for x in elements)
        else:
            element_list = elements
                
        pm.py_send('*expand_elements', element_list) 
        if type(elements)!=str: 
           pm.py_send('#') 