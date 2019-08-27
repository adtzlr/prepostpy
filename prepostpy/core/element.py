# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: dutzi
"""


import numpy as np
import py_mentat as pm

from .node import Node

class Element:
    
    def __init__(self,category,connectivity,*args,**kwargs):
        
        self.category = category
        self.connectivity = connectivity
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value

    def tomentat(self):
        if isinstance(self.connectivity[0],Node):
            conns = ' '.join(str(x.mentat_id) for x in self.connectivity)
        else:
            conns = ' '.join(str(x) for x in self.connectivity)

        cdict = {'Hex (8)':'hex8',
                 'Quad (4)': 'quad4',
                 'Tria (3)': 'tria3'}
            
        pm.py_send('*set_element_class', cdict[self.category])
        pm.py_send('*add_elements', conns)
        
        mentat_id =  pm.py_get_int('max_element_id()')
        
        try:
            element_set = self.options['membership']
            end = ' #'

            mentat_command = ' '.join(['*store_elements', 
                                       element_set, str(mentat_id), end])
            pm.py_send(mentat_command)
        except:
            pass
        
        self.mentat_id = mentat_id