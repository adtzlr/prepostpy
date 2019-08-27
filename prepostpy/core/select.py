# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 15:25:50 2019

@author: dutzi
"""

import py_mentat as pm
import numpy as np

class Select:
    
    def __init__(self):
        self.Box = Box()
        self.Set = Set()
        
class Set:
    
    def __init__(self):
        pass
    
    def select(self,membership):
        pm.py_send('*select_sets %s' % membership)
        
class Box:
    
    def __init__(self):
        self.xlim = [0,np.inf]
        self.ylim = [0,0]
        self.zlim = [0,0]
        
    def select(self,objects='Nodes',xlim=None,ylim=None,zlim=None,clear=False,reset=False):
        if xlim is not None: self.xlim = xlim
        if ylim is not None: self.ylim = ylim
        if zlim is not None: self.zlim = zlim
        limits = *self.xlim, *self.ylim, *self.zlim
        
        if clear:
            self.clear()
        if reset:
            self.reset()
        
        pm.py_send('*select_method_box')
        pm.py_send('*select_%s %s %s %s %s %s %s' % (objects.lower(), *limits))
           
    def reset(self):
        pm.py_send('*select_reset')
         
    def clear(self,objects=''):
        if objects is not '':
            obj = '_'+objects
        else:
            obj = objects
        pm.py_send('*select_clear'+obj.lower())
        
    def select_x(self,objects='Nodes',y=0.0,z=0.0,clear=False,reset=False):
        self.xlim = [-np.inf,np.inf]
        self.ylim = [y,y]
        self.zlim = [z,z]
        if clear:
            self.clear()
        if reset:
            self.reset()
        self.select(objects)
        
    def select_y(self,objects='Nodes',x=0.0,z=0.0,clear=False,reset=False):
        self.ylim = [-np.inf,np.inf]
        self.xlim = [x,x]
        self.zlim = [z,z]
        if clear:
            self.clear()
        if reset:
            self.reset()
        self.select(objects)
        
    def select_z(self,objects='Nodes',x=0.0,y=0.0,clear=False,reset=False):
        self.zlim = [-np.inf,np.inf]
        self.xlim = [x,x]
        self.ylim = [y,y]
        if clear:
            self.clear()
        if reset:
            self.reset()
        self.select(objects)
        
    def select_xy(self,objects='Nodes',z=0.0,tol=1e-6,clear=False,reset=False):
        self.xlim = [-np.inf,np.inf]
        self.ylim = [-np.inf,np.inf]
        self.zlim = [z-tol,z+tol]
        if clear:
            self.clear()
        if reset:
            self.reset()
        self.select(objects)
        
    def select_yz(self,objects='Nodes',x=0.0,tol=1e-6,clear=False,reset=False):
        self.xlim = [x-tol,x+tol]
        self.ylim = [-np.inf,np.inf]
        self.zlim = [-np.inf,np.inf]
        if clear:
            self.clear()
        if reset:
            self.reset()
        self.select(objects)
        
    def select_zx(self,objects='Nodes',y=0.0,tol=1e-6,clear=False,reset=False):
        self.xlim = [-np.inf,np.inf]
        self.ylim = [y-tol,y+tol]
        self.zlim = [-np.inf,np.inf]
        if clear:
            self.clear()
        if reset:
            self.reset()
        self.select(objects)