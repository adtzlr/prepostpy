# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: dutzi
"""


#import numpy as np
import py_mentat as pm

from .node import Node
from .select import NextNodes

class Links:
    
    def __init__(self):
        self.RBE2 = RBE2()

class RBE2:
    
    def __init__(self,*args,**kwargs):
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value

    def new(self,label,node,tied_nodes,dof):
        
        
        
        if isinstance(tied_nodes[0],Node):
            tnodes = ' '.join(str(x.mentat_id) for x in tied_nodes)
        elif tied_nodes[0].lower() == 'next':
            options = {'only': 'Surface', 
                       'clear': True, 
                       'reset': True, 
                       'extend': True,
                       'axes': [0,1,2]}
            if len(tied_nodes) == 3:
                options_user = tied_nodes[-1]
                for k,v in options_user.items():
                    options[k] = v

            NextNodes().select(centroid=node.coordinates,nnodes=tied_nodes[1],
                             **options)    
            tnodes = ' all_selected'
        else:
            tnodes = ' '.join(str(x) for x in tied_nodes)
            
        tnodes = tnodes+' #'
            
        if isinstance(node,Node):
            n = str(node.mentat_id)
        else:
            n = str(node)
            
        pm.py_send('*new_rbe2')
        pm.py_send('*rbe2_name', label)
        pm.py_send('*rbe2_ret_node', n)
        
        for i,d in enumerate(dof):
            if bool(d) is True:
                pm.py_send('*rbe2_tied_dof %s' % str(i+1))
            
        pm.py_send('*add_rbe2_tied_nodes', tnodes)