# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: dutzi
"""


import numpy as np
import py_mentat as pm
from .point import Point

class Curve:
    
    def __init__(self,category,connectivity,*args,**kwargs):
        
        self.category = category
        self.connectivity = np.array(connectivity)
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value

    def tomentat(self):
        conns_flat = self.connectivity.flatten()
        if isinstance(conns_flat[0],Point):
            if 'Arc' in self.category or 'Circle' in self.category: # point coordinates
                conns = ' '.join(' '.join(str(y) for y in x.coordinates) for x in conns_flat)
            else: # point numbers
                conns = ' '.join(str(x.mentat_id) for x in conns_flat)
        else:
            conns = ' '.join(str(x) for x in conns_flat)
        
        cdict = {'Line': 'line',
                 'Bezier': 'bezier',
                 'Cubic Spline':'cubic_spline',
                 'NURBS': 'nurb',
                 'Polyline':'polyline',
                 'Composite':'composite',
                 'Circle Cen/Pnt':'circle_cp',
                 'Arc Cen/Pnt/Pnt':'arc_cpp'}
                 
        pm.py_send('*set_curve_type', cdict[self.category])
        pm.py_send('*add_curves', conns)
        
        mentat_id =  pm.py_get_int('max_curve_id()')
        self.mentat_id = mentat_id
        
        try:
            element_set = self.options['membership']
            mentat_command = ' '.join(['*store_curves', 
                                       element_set, str(mentat_id), ' #'])
            pm.py_send(mentat_command)
        except:
            pass
        
        mentat_command = ' '.join(['*apply_curve_divisions', 
                                   str(self.mentat_id), ' #'])
        
        try:
            curve_div = self.options['Divisions']
            pm.py_send('*set_curve_div_type_fix_ndiv')
            pm.py_send('*set_curve_div_num', str(curve_div))
            pm.py_send(mentat_command)
        except:
            pass
        
        try:
            target_length = self.options['Length']
            pm.py_send('*set_curve_div_type_fix_avgl')
            pm.py_send('*set_curve_div_avgl', str(target_length))
            pm.py_send(mentat_command)
        except:
            pass
        
        try:
            l2l1 = self.options['Ratio']
            pm.py_send('*set_curve_div_type_variable_l1l2')
            pm.py_send('*set_curve_div_opt_ndiv_l2l1_ratio')
            pm.py_send('*set_curve_div_l2l1_ratio', str(l2l1))
            pm.py_send(mentat_command)
        except:
            pass