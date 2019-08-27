# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: dutzi
"""


import numpy as np
import py_mentat as pm
import time

from .element import Element

class Job:
    
    def __init__(self,label,loadcases=[], category='structural', 
                 jobresults_tensor=['Cauchy Stress','Total Strain'],
                 jobresults_scalar=[],
                 non_positive_definite=True,
                 threads=1,*args,**kwargs):
        
        self.label = label
        self.category = category
        self.loadcases = loadcases
        self.jobresults_tensor = jobresults_tensor
        self.jobresults_scalar = jobresults_scalar
        self.filename = ''
        self.non_positive_definite = non_positive_definite
        self.threads = threads
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value

    def set_element_type(self, etype, elements='all_existing'):
        pm.py_send('*element_type %d %s' % (etype, elements))
        
    def write_input(self):
        pm.py_send('*edit_job', self.label)
        pm.py_send('*job_write_input yes')
        
    def check(self):
        pm.py_send('*edit_job', self.label)
        pm.py_send('*check_job')
        
    def tomentat(self):
        
        tdict = {'cauchy stress': 'cauchy',
                 'stress': 'stress',
                 'deformation gradient': 'deform_grad',
                 'total strain': 'strain',
                 'logarithmic strain': 'log_strain',
                 'elastic left cauchy-green deformation': 'el_leftcg_deform'}
                 
        sdict = {'equivalent von mises stress': 'von_mises',
                 'determinant of deformation gradient': 'det_deform_grad'}
        
        pm.py_send('*prog_use_current_job on *new_job', self.category)
        pm.py_send('*job_name', self.label)
        for lc in self.loadcases:
            if type(lc) == str:
                label = lc
            else:
                label = lc.label
            pm.py_send('*add_job_loadcases', label)
            
        for tensor in self.jobresults_tensor:
             pm.py_send('*add_post_tensor', tdict[tensor.lower()])
             
        for scalar in self.jobresults_scalar:
             pm.py_send('*add_post_var', sdict[scalar.lower()])
            
        for key,value in self.options.items():
            pm.py_send('*job_option %s:%s' % (key,value))
            
        if self.non_positive_definite:
            pm.py_send('*job_option nonpos:on')
            
        if self.threads > 1:
            pm.py_send('*job_option assem_recov_multi_threading:on')
            pm.py_send('*job_option mfront_sparse_multi_threading:on')
        if self.threads > 2:
            pm.py_send('*job_param assem_recov_nthreads %d' % self.threads)
            pm.py_send('*job_param nthreads %d' % self.threads)
            
    def submit(self,monitor=False,verbose=0):
        self.joblist = []
        njobs = pm.py_get_int('njobs()')
        for j in range(njobs):
            joblabel = pm.py_get_string('job_name_index(%d)' % j)
            self.joblist.append(joblabel)
        self.mentat_id = self.joblist.index(self.label)+1
        pm.py_send('*submit_job %d' % self.mentat_id)
        
        stsfile = '.'.join(self.filename.split('.')[:-1])+'_'+self.label+'.sts'
        
        if monitor:
            pm.py_send('*monitor_job')
        else:
            # pause script while job is running
            while True:
                # check every 5 seconds if job has finished by evaluating
                # model_job##.sts file
                time.sleep(5)
                with open(stsfile,'r') as f1:
                    lines = f1.readlines()
                    try: # catch error if less than 3 lines are present
                        exit_message = lines[-3]
                    except:
                        exit_message = ''
                
                # check if job has finished
                if '3004' in exit_message:
                    if verbose > 0: print(exit_message)
                    break
                else: # print current loadcase and increment
                    try: # catch error if the last line does not contain the progress
                        lc = int(lines[-1][:7])
                        inc = int(lines[-1][7:15])
                        progress = 'current loadcase %d / inc. %d' % (lc, inc)
                        if verbose > 0: print(progress)
                    except:
                        pass