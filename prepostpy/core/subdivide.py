# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:08:52 2019

@author: dutzi
"""

import numpy as np
import py_mentat as pm

class Subdivide:
    
    def __init__(self):
        self.divisions = np.array([2,2,2])
        self.bias_factors = np.array([0,0,0])
        
    def subdivide(self,objects='Elements'):
        xi = ['u','v','w']
        for x,v in zip(xi,self.divisions):
            pm.py_send('*sub_uvwdiv  %s %s' % (x, str(v)))
        for x,v in zip(xi,self.bias_factors):
            pm.py_send('*sub_bias_uvwfactors %s %s' % (x, str(v)))
            
        sdict = {'Elements':'elements',
                 'Curves':'curves_real'}

        move_command = '*subdivide_'+sdict[objects]+' all_existing'
        pm.py_send(move_command) 
        
    def reset(self):
        pm.py_send('*subdivide_reset')