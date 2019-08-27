# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:08:52 2019

@author: dutzi
"""

import py_mentat as pm

class Sweep:
    
    def __init__(self):
        pass
        
    def sweep(self,objects='all'):
        sweep_command = '*sweep_'+objects
        if objects != 'all':
            sweep_command = sweep_command + ' all_existing'
        pm.py_send(sweep_command)