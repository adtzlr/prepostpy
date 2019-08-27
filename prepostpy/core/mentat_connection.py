# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: dutzi
"""


import numpy as np
import py_mentat as pm
import time
import os
import psutil

import subprocess

class MentatConnection:
    def __init__(self, msc_path = r'C:\MSC.Software',
                 version = 'latest', #r'2018.0.0'
                 startmentat = True,
                 killmentat = False,
                 quitmentat = False,
                 background = False,
                 disconnect = True,
                 ):
        self.msc_path = msc_path
        self.startmentat = startmentat
        self.killmentat = killmentat
        self.quitmentat = quitmentat
        self.disconnect = disconnect
        self.connection = False
        
        # select latest installed version of mentat
        if version == 'latest':
            self._get_installed_version()
        else:
            self.mentat_version = version
            
        self.mentat_year = self.mentat_version.split('.')[0]
        self.mentat_path = self.msc_path+r'\Marc'+'\\'+ \
                           self.mentat_version+r'\mentat'+self.mentat_year+ \
                           r'\bin\mentat.bat'
        self.callmentat = [self.mentat_path, '-pr', 
                           os.getcwd()+'\\'+r'mentat_pyconnect.proc']
        # 'cmd.exe /C', 
        self.background = background
        if self.background:
            self.callmentat.append('-bg')
            
    def _get_installed_version(self):
        self.mentat_version = next(os.walk(self.msc_path+r'\Marc'))[1][-1]
    
    def __enter__(self):
        
        if self.killmentat:
            PROCNAME = "mentatOGL.exe"
            for proc in psutil.process_iter():
                # check whether the process name matches
                if proc.name() == PROCNAME:
                    proc.kill()
        
        if self.startmentat:
            
            # connect to mentat
            #if self.background:
            #    CREATE_NO_WINDOW = 0x08000000
            #    si = subprocess.STARTUPINFO()
            #    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            #else:
            #    CREATE_NO_WINDOW = 0
            #    si = None
                
            subprocess.Popen(r' '.join(self.callmentat),
                             stdout=subprocess.PIPE, 
                             stderr = subprocess.PIPE)#,
                             #startupinfo = si)
                             #creationflags=CREATE_NO_WINDOW) #, stdout=subprocess.PIPE
            #out,err = p.communicate()
            
            while True:
                try:
                    pm.py_connect("127.0.0.1", 40007)
                    # test connection
                    pm.py_send("test connection")
                    break
                except:
                    time.sleep(0.25)
                    
            self.connection = True
            
        elif not self.startmentat and not self.connection:
            pm.py_connect("127.0.0.1", 40007)
            self.connection = True
            
        return self
        
    def __exit__(self, H_type, H_value, H_traceback):
        if self.quitmentat:
            pm.py_send("*quit yes")
            self.connection = False
        if self.disconnect:
            pm.py_disconnect()
            self.connection = False
        #pass