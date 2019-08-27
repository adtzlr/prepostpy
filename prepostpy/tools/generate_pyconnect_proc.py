# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 14:30:20 2019

@author: dutzi
"""

import os

def generate_proc(path=''):
    
    fname = 'mentat_pyconnect.proc'
    path = os.getcwd()
    fullfname = path+'\\'+fname
        
    with open(fullfname, 'w') as out:
        out.write('*py_separate_process on \n')
        out.write('*py_connect')
    