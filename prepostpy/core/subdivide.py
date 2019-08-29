# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:08:52 2019

@author: dutzi
"""

import numpy as np
import py_mentat as pm

from .element import Element

class Subdivide:
    
    def __init__(self):
        self.divisions = np.array([2,2,2])
        self.bias_factors = np.array([0,0,0])
        
    def subdivide(self,elements,objects='Elements',
                  divisions=[2,2,2],
                  bias_factors=[0,0,0]):
        
        self.divisions = divisions
        self.bias_factors = bias_factors
        
        xi = ['u','v','w']
        for x,v in zip(xi,self.divisions):
            pm.py_send('*sub_uvwdiv  %s %s' % (x, str(v)))
        for x,v in zip(xi,self.bias_factors):
            pm.py_send('*sub_bias_uvwfactors %s %s' % (x, str(v)))
            
        sdict = {'Elements':'elements',
                 'Curves':'curves_real'}
                 
        if type(elements)!=str:
            if isinstance(elements[0],Element):
                element_list = ' '.join(str(x.mentat_id) for x in elements)
            else:
                element_list = ' '.join(str(x) for x in elements)
        else:
            element_list = elements

        subdivide_command = '*subdivide_'+sdict[objects]+' '+element_list
        pm.py_send(subdivide_command) 
        
    def reset(self):
        self.divisions = np.array([2,2,2])
        self.bias_factors = np.array([0,0,0])
        pm.py_send('*subdivide_reset')