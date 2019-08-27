# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: dutzi
"""


import numpy as np
import py_mentat as pm

class Table:
    
    def __init__(self,label,category='time',points=np.zeros((0,2)),
                 *args,**kwargs):
        
        self.label = label
        self.category = category
        self.points = points
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value

    def add_point(self,point):
        self.points = np.vstack((self.points,point))
        
    def tomentat(self):
        pm.py_send('*new_md_table 1 1')
        pm.py_send('*table_name', self.label)
        pm.py_send('*set_md_table_type 1', self.category)
        for point in self.points:
            p = ' '.join(str(coord) for coord in point)
            pm.py_send('*table_add', p)
            

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

class Element:
    
    def __init__(self,category,connectivity,*args,**kwargs):
        
        self.category = category
        self.connectivity = connectivity
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value

    def tomentat(self):
        conns = ' '.join(str(x) for x in self.connectivity)
        pm.py_send('*set_element_class', self.category)
        pm.py_send('*add_elements', conns)
        
        mentat_id =  pm.py_get_int('max_element_id()')
        
        try:
            element_set = self.options['membership']
            end = ' #'

            mentat_command = ' '.join(['*store_elements', 
                                       element_set, str(mentat_id), end])
            pm.py_send(mentat_command)
        except:
            pass
        
        self.mentat_id = mentat_id

class Boundary:
    
    def __init__(self,label,category,dof,dof_values=np.zeros(6),nodes=[],tables={},*args,**kwargs):
        
        self.label = label
        self.dof = np.array(dof).astype(int)
        self.dof_values = dof_values
        self.nodes = nodes
        self.category = category
        self.tables= tables
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value

    def tomentat(self):
        pm.py_send('*new_apply *apply_type', self.category)
        pm.py_send('*apply_name', self.label)
        
        if self.category == 'fixed_displacement':
            self.dof_labels = ['x','y','z','rx','ry','rz']
        if self.category == 'point_load': 
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
        
class Material:
    
    def __init__(self,label,category='elast_plast_iso',elements=[],*args,**kwargs):
        
        self.label = label
        self.category = category
        self.elements = elements
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value
        
    def tomentat(self):
        
        pm.py_send('*new_mater standard *mater_option general:state:solid \
                    *mater_option general:skip_structural:off')
        pm.py_send('*mater_name', self.label)
        pm.py_send('*edit_mater', self.label)
        
        if self.category == 'elast_plast_iso':
            E  = self.options['E']
            nu = self.options['nu']
            pm.py_send('*mater_param structural:youngs_modulus', str(E))
            pm.py_send('*mater_param structural:poissons_ratio', str(nu))
            
        if type(self.elements) == str:
            n = self.elements
        else:
            n = ' '.join(str(a) for a in self.elements)+' #'
            
        pm.py_send('*add_mater_elements %s' % n)
        
class Loadcase:
    
    def __init__(self,label,category='struc:static',*args,**kwargs):
        
        self.label = label
        self.category = category
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value
        
    def tomentat(self):
        pm.py_send('*new_loadcase *loadcase_type', self.category)
        pm.py_send('*loadcase_name', self.label)
        
class Job:
    
    def __init__(self,label,loadcases=[], category='structural',*args,**kwargs):
        
        self.label = label
        self.category = category
        self.loadcases = loadcases
        
        self.options = {}
        for key,value in kwargs.items():
            self.options[key] = value
        
    def tomentat(self):
        pm.py_send('*prog_use_current_job on *new_job', self.category)
        pm.py_send('*job_name', self.label)
        for lc in self.loadcases:
            if type(lc) == str:
                label = lc
            else:
                label = lc.label
            pm.py_send('*add_job_loadcases', label)
            
        for key,value in self.options.items():
            pm.py_send('*job_option %s:%s' % (key,value))
            
    def submit(self):
        self.joblist = []
        njobs = pm.py_get_int('njobs()')
        for j in range(njobs):
            joblabel = pm.py_get_string('job_name_index(%d)' % j)
            self.joblist.append(joblabel)
        self.mentat_id = self.joblist.index(self.label)+1
        pm.py_send('*submit_job %d' % self.mentat_id)# %  *monitor_job

class File:
    def __init__(self,filename):
        self.filename = filename
        self.objects = []

    def add(self,o):
        self.objects.append(o)
        
    def savefile(self):
        pm.py_send(r'*save_as_model '+self.filename+' yes')
        
    def tomentat(self):
        
        #reset model
        pm.py_send("*new_model")
        pm.py_send("yes")
        
        for o in self.objects:
            o.tomentat()

class MentatConnection:
    def __init__(self):
        pass
    
    def __enter__(self):
        # connect to mentat
        pm.py_connect("127.0.0.1", 40007)
        return self
        
    def __exit__(self, H_type, H_value, H_traceback):
        pm.py_disconnect()
        
            
F = File(filename=r'C:\Users\adutzler\Desktop\test\modelx.mfd')

T1 = Table(label='Table1', category='time')
T1.add_point([0,0])
T1.add_point([1,1])

B1 = Boundary(label='Fixed1',
              category='fixed_displacement',
              dof=[1,1,1,0,0,0],
              dof_values=[0,0,0,0,0],
              nodes='nodes_left')

B2 = Boundary(label='Fixed2',
              category='fixed_displacement',
              dof=[1,1,1,0,0,0],
              dof_values=[1,0,0,0,0],
              nodes='nodes_right', 
              ramp='off',
              tables={'x':T1})

M1 = Material(label='material1',
              category='elast_plast_iso',
              elements=[1], 
              E=210000,nu=0.3)


dx,dy,dz = 1,1,1
F.add(Node([ 0, 0, 0],membership='nodes_left'))
F.add(Node([dx, 0, 0],membership='nodes_right'))
F.add(Node([dx,dy, 0],membership='nodes_right'))
F.add(Node([ 0,dy, 0],membership='nodes_left'))
F.add(Node([ 0, 0,dz],membership='nodes_left'))
F.add(Node([dx, 0,dz],membership='nodes_right'))
F.add(Node([dx,dy,dz],membership='nodes_right'))
F.add(Node([ 0,dy,dz],membership='nodes_left'))

F.add(Element(category='hex8',
                  connectivity=[1,2,3,4,5,6,7,8],
                  membership='elements_A'))

F.add(T1)   
F.add(M1)
F.add(B1)
F.add(B2)
LC = Loadcase('lc1')
F.add(Loadcase('lc1'))
F.add(Job('joba',loadcases=[LC],strain='large'))
F.add(Job('jobb',loadcases=['lc1'],strain='large'))

with MentatConnection():
    F.tomentat()
    F.savefile()
    F.objects[-1].submit()

