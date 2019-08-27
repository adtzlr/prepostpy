# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: adutz
"""

import numpy as np
import py_mentat as pm

class Node:
    
    def __init__(self,coordinates,*args,**kwargs):
        
        self.coordinates = np.array(coordinates)
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value

        self.mentat_id = None

    def tomentat(self):
        x,y,z = self.coordinates
        pm.py_send("*add_nodes %f %f %f" % (x,y,z))
        
        mentat_id =  pm.py_get_int('max_node_id()')
        
        try:
            node_set = self.options['membership']
            end = ' #'

            mentat_command = ' '.join(['*store_nodes', 
                                       node_set, str(mentat_id), end])
            pm.py_send(mentat_command)
        except:
            pass
        
        self.mentat_id = mentat_id