# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: dutzi
"""


import numpy as np
import py_mentat as pm

class Boundary:
    
    def __init__(self,label='',category='Fixed Displacement',dof=np.zeros(6),dof_values=np.zeros(6),nodes=[],tables={},*args,**kwargs):
        
        if 'symmetry' in label.lower():
            dof=np.zeros(6)
            dof_values=np.zeros(6)
            nodes=[]
            tables={}
            category='Fixed Displacement'
            
        self.label = label
        self.dof = np.array(dof).astype(int)
        self.dof_values = dof_values
        self.nodes = nodes
        self.category = category
        self.tables= tables
        
        if 'symmetry' in self.label.lower():
            self.symmetry(self.label.lower()[-1])

        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value

    def symmetry(self,x):
        cdict = {'x':(0,4,5), 'y':(1,3,5), 'z':(2,3,4)}
        np.put(self.dof, cdict[x], 1)

    def tomentat(self):
        cdict = {'Fixed Displacement':'fixed_displacement',
                 'Point Load':'point_load'}
        pm.py_send('*new_apply *apply_type', cdict[self.category])
        pm.py_send('*apply_name', self.label)
        
        if self.category == 'Fixed Displacement':
            self.dof_labels = ['x','y','z','rx','ry','rz']
        if self.category == 'Point Load': 
            self.dof_labels = ['x','y','z','mx','my','mz']

        for i,(d,l,v) in enumerate(zip(self.dof,self.dof_labels,self.dof_values)):
            if d == 1: 
                pm.py_send('*apply_dof %s  \
                            *apply_dof_value %s %s' % (l, l, str(v)))
        
        if type(self.nodes) == str:
            n = self.nodes
        else:
            n = ' '.join(str(a) for a in self.nodes)+' #'
            
        pm.py_send('*add_apply_nodes %s' % n)
                
        try:
            rdict = {'on': 'current_to_target',
                     'off': 'off'}
            ramp = rdict[self.options['ramp']]
            pm.py_send('*apply_option ramp:%s' % ramp)
        except:
            pass
        
        for key,table in self.tables.items():
            pm.py_send('*apply_dof_table %s %s' % (key, table.label))
            #print('*apply_dof_table %s %s' % (key, table.label))
        
        #mentat_id =  pm.py_get_int('max_node_id()')
        #self.mentat_id = mentat_id
        
    def add_nodes(self,nodes):
        self.nodes = nodes
        pm.py_send('*edit_apply %s' % self.label)
        if type(self.nodes) == str:
            n = self.nodes
        else:
            n = ' '.join(str(a) for a in self.nodes)+' #'
            
        pm.py_send('*add_apply_nodes %s' % n)