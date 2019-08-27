# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:08:52 2019

@author: dutzi
"""

import py_mentat as pm
from .curve import Curve
import time

class Automesh:
    
    def __init__(self):
        self.Planar = _Planar()
    
class _Planar:
    
    def __init__(self):
        self.Overlay = _Overlay()
        self.AdvancedFront = _AdvancedFront()
        self.Delauney = _Delauney()
    
class _Overlay:
    
    def __init__(self):
        
        self.divisions = 10, 10
        self.bias = 0, 0
        
    def quad_mesh(self,curves):
        if isinstance(curves[0],Curve):
            curve_list = ' '.join(str(x.mentat_id) for x in curves)
        else:
            curve_list = ' '.join(str(x) for x in curves)
        pm.py_send('*overlay_mesh', curve_list)
        pm.py_send('#')
        
class _AdvancedFront:
    
    def __init__(self):
        pass
        
    def quad_mesh(self,curves,*args,**kwargs):
        if isinstance(curves[0],Curve):
            curve_list = ' '.join(str(x.mentat_id) for x in curves)
        else:
            curve_list = ' '.join(str(x) for x in curves)
            
        n1 = pm.py_get_int('max_element_id()')
        
        pm.py_send('*af_planar_quadmesh %s #' % curve_list)
        
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value
        
        try:
            element_set = self.options['membership']
            #end = ' #'
            n2 = pm.py_get_int('max_element_id()')
            
            #elements = list(range(n1+1,n2+1))
            #elem = ' '.join(str(x) for x in elements)
            elem = str(n1)+' to '+str(n2)

            mentat_command = ' '.join(['*store_elements', 
                                       element_set, elem])
            pm.py_send(mentat_command)
        except:
            pass
        
    def quad_tri_mesh(self,curves,max_quad_distortion=0.9,*args,**kwargs):
        if isinstance(curves[0],Curve):
            curve_list = ' '.join(str(x.mentat_id) for x in curves)
        else:
            curve_list = ' '.join(str(x) for x in curves)
            
        n1 = pm.py_get_int('max_element_id()')
        
        pm.py_send('*af_set_max_quad_distortion', str(max_quad_distortion))
        pm.py_send('*af_planar_quad_trimesh', curve_list)
        pm.py_send('#')
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value
        
        try:
            element_set = self.options['membership']
            end = ' #'
            
            n2 = pm.py_get_int('max_element_id()')
            
            elements = list(range(n1+1,n2+1))
            elem = ' '.join(str(x) for x in elements)

            mentat_command = ' '.join(['*store_elements', 
                                       element_set, elem, end])
            pm.py_send(mentat_command)
        except:
            pass
        
    def tri_mesh(self,curves):
        if isinstance(curves[0],Curve):
            curve_list = ' '.join(str(x.mentat_id) for x in curves)
        else:
            curve_list = ' '.join(str(x) for x in curves)
        pm.py_send('*af_planar_trimesh', curve_list)
        pm.py_send('#')
        
class _Delauney:
    
    def __init__(self):
        pass
        
    def tri_mesh(self,curves):
        if isinstance(curves[0],Curve):
            curve_list = ' '.join(str(x.mentat_id) for x in curves)
        else:
            curve_list = ' '.join(str(x) for x in curves)
        pm.py_send('*dt_planar_trimesh', curve_list)
        pm.py_send('#')