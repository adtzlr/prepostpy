# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: dutzi
"""


import numpy as np
import py_mentat as pm

class Material:
    
    def __init__(self,label,category='elast_plast_iso',elements=[],*args,**kwargs):
        
        self.label = label
        self.category = category
        self.elements = elements
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value

    def set_param(self,p):
        try:
            v = self.options[p]
        except:
            v = 0.0
        return v
        
    def tomentat(self):
        
        cdict = {'Elastic-Plastic Isotropic':'elast_plast_iso',
                 'Mooney':'mooney'}
        
        pm.py_send('*new_mater standard *mater_option general:state:solid \
                    *mater_option general:skip_structural:off')
        pm.py_send('*mater_option structural:type:%s' % cdict[self.category])
        #pm.py_send('*edit_mater', self.label)
        pm.py_send('*mater_name', self.label)

        if self.category == 'Elastic-Plastic Isotropic':
            E  = self.set_param('E')
            nu = self.set_param('nu')
            pm.py_send('*mater_param structural:youngs_modulus', str(E))
            pm.py_send('*mater_param structural:poissons_ratio', str(nu))
            
        if self.category == 'Mooney':
            C10  = self.set_param('C10')
            C01  = self.set_param('C01')
            C11  = self.set_param('C11')
            C20  = self.set_param('C20')
            C30  = self.set_param('C30')
            pm.py_send('*mater_param structural:mooney_c10', str(C10))
            pm.py_send('*mater_param structural:mooney_c01', str(C01))
            pm.py_send('*mater_param structural:mooney_c11', str(C11))
            pm.py_send('*mater_param structural:mooney_c20', str(C20))
            pm.py_send('*mater_param structural:mooney_c30', str(C30))
            
            alpha = self.set_param('alpha')
            if alpha != 0:
                pm.py_send('*mater_option structural:thermal_expansion:on')
                pm.py_send('*mater_param structural:thermal_exp', str(alpha))
            
        if type(self.elements) == str:
            n = self.elements
        else:
            n = ' '.join(str(a) for a in self.elements)+' #'
            
        pm.py_send('*add_mater_elements %s' % n)
        
    def add_elements(self,elements):
        self.elements = elements
        pm.py_send('*edit_mater %s' % self.label)
        if type(self.elements) == str:
            n = self.elements
        else:
            n = ' '.join(str(a) for a in self.elements)+' #'
            
        pm.py_send('*add_mater_elements %s' % n)