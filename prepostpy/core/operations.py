# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 15:25:50 2019

@author: dutzi
"""

#import py_mentat as pm
from .sweep import Sweep
from .expand import Expand
from .move import Move
from .symmetry import Symmetry
from .subdivide import Subdivide
from .change import ChangeClass

class Operations:
    
    def __init__(self):
        self.Sweep = Sweep()
        self.Expand = Expand()
        self.Move = Move()
        self.Symmetry = Symmetry()
        self.Subdivide = Subdivide()
        self.ChangeClass = ChangeClass()