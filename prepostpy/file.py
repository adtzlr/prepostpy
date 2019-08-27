# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: dutzi
"""

import subprocess
import time
import os
import numpy as np
from types import SimpleNamespace

import py_mentat as pm

from .core import Table
from .core import Point
from .core import Curve
from .core import Node
from .core import Material
from .core import Element
from .core import Boundary
from .core import Loadcase
from .core import Job
from .core import Automesh
#from .expand import Expand
#from .sweep import Sweep
from .core import Select
from .core import Operations
from .core import Links
from .tools import generate_proc
#from .post_file import PostFile

class File:
    def __init__(self,filename):
        self.filename = filename
        self.filepath = '\\'.join(self.filename.split('\\')[:-1])
        self.tables = []
        self.points = []
        self.curves = []
        self.surfaces = []
        self.nodes = []
        self.elements = []
        self.boundaries = []
        self.materials = []
        self.loadcases = []
        self.jobs = []
        self.Automesh = Automesh()
        #self.Expand = Expand()
        #self.Sweep = Sweep()
        self.Operations = Operations()
        self.Select = Select()
        self.Links = Links()
        self.exported = False
        self.item = SimpleNamespace()
        
        generate_proc()
        
        #self.PostFile = PostFile()
        
    def reset(self):
        self.tables = []
        self.points = []
        self.curves = []
        self.surfaces = []
        self.nodes = []
        self.elements = []
        self.boundaries = []
        self.materials = []
        self.loadcases = []
        self.jobs = []
        
    def build(self):
        self.reset()
        for k,o in sorted(vars(self.item).items()):
            if isinstance(o,Point): self.points.append(o)
            if isinstance(o,Curve): self.curves.append(o)
            if isinstance(o,Node): self.nodes.append(o)
            if isinstance(o,Element): self.elements.append(o)
            if isinstance(o,Table): self.tables.append(o)
            if isinstance(o,Material): self.materials.append(o)
            if isinstance(o,Boundary): self.boundaries.append(o)
            if isinstance(o,Loadcase): self.loadcases.append(o)
            if isinstance(o,Job): self.jobs.append(o)

    def __add(self,ob):
        
        try :
            len(ob)
            obj = ob
        except:
            obj = [ob]
            
        for o in obj:
            if isinstance(o,Point): self.points.append(o)
            if isinstance(o,Curve): self.curves.append(o)
            if isinstance(o,Node): self.nodes.append(o)
            if isinstance(o,Element): self.elements.append(o)
            if isinstance(o,Table): self.tables.append(o)
            if isinstance(o,Material): self.materials.append(o)
            if isinstance(o,Boundary): self.boundaries.append(o)
            if isinstance(o,Loadcase): self.loadcases.append(o)
            if isinstance(o,Job): self.jobs.append(o)
        
    def savefile(self,write_input=True):
        pm.py_send(r'*save_as_model '+self.filename+' yes')
        if write_input:
            for job in self.jobs:
                job.write_input()
        
    def tomentat(self):
        self.build()
        #reset model
        pm.py_send("*new_model yes")
        #pm.py_send("yes")
        
        self.objects =  [*self.points,
                         *self.curves,
                         *self.nodes,
                         *self.elements,
                         *self.tables,
                         *self.materials,
                         *self.boundaries,
                         *self.loadcases,
                         *self.jobs]
                         
        for o in self.objects:
            o.tomentat()
            
        for j in self.jobs:
            j.filename = self.filename
            
        self.exported = True
        
    def _get_installed_version(self,msc_path):
        return next(os.walk(msc_path+r'\Marc'))[1][-1]
        
    def submit(self,job,verbose=1,
               msc_path=r'C:\MSC.Software',version='latest',threads=1,
               scratch_dir=None):

        workdir = '\\'.join(self.filename.split('\\')[:-1])
        stsfile = '.'.join(self.filename.split('.')[:-1])+'_'+job.label+'.sts'
        datfile = '.'.join(self.filename.split('.')[:-1])+'_'+job.label+'.dat'
        
        # select latest installed version of mentat
        if version == 'latest':
            marc_version = self._get_installed_version(msc_path)
        else:
            marc_version = version
            
        marc_year = marc_version.split('.')[0]
        marc_path = msc_path+r'\Marc'+'\\'+ \
                           marc_version+r'\marc'+marc_year+ \
                           r'\tools\run_marc.bat'
        runjob = [marc_path, '-jid', datfile, '-dir', workdir]

        if threads > 1:
            runjob += ['-nts', str(threads), '-nte', str(threads)]
        if scratch_dir is not None:
            runjob += ['-sdir', scratch_dir]

        subprocess.run(r' '.join(runjob),
                             stdout=subprocess.PIPE, 
                             stderr = subprocess.PIPE)
        
        if verbose > 0:
            with open(stsfile,'r') as f1:
                lines = f1.readlines()
                exit_message = lines[-3]
            #check if job has finished
            if '3004' in exit_message:
                print('Job completed sucessful (Exit 3004).')
            else:
                raise ValueError('Job error.', exit_message)
        
        # 'cmd.exe /C',

#        # pause script while job is running
#        while True:
#            # check every 5 seconds if job has finished by evaluating
#            # model_job##.sts file
#            time.sleep(5)
#            with open(stsfile,'r') as f1:
#                lines = f1.readlines()
#                try: # catch error if less than 3 lines are present
#                    exit_message = lines[-3]
#                except:
#                    exit_message = ''
#            
#            # check if job has finished
#            if '3004' in exit_message:
#                if verbose > 0: print(exit_message)
#                break
#            else: # print current loadcase and increment
#                try: # catch error if the last line does not contain the progress
#                    lc = int(lines[-1][:7])
#                    inc = int(lines[-1][7:15])
#                    progress = 'current loadcase %d / inc. %d' % (lc, inc)
#                    if verbose > 0: print(progress)
#                except:
#                    pass