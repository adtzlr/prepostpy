# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 15:25:50 2019

@author: dutzi
"""

import py_mentat as pm
import numpy as np

class Select:
    
    def __init__(self):
        self.Box = Box()
        self.PointDistance = PointDistance()
        self.Set = Set()
        self.NextNodes = NextNodes()
        
class Set:
    
    def __init__(self):
        pass
    
    def select(self,membership):
        pm.py_send('*select_sets %s' % membership)
        
class FaceFlood:
    
    def __init__(self):
        pass
    
    def select(self,element):
        pm.py_send('*select_method_face_flood')
        
        for i in range(4):
            pm.py_send('*select_nodes %d:%d' % (element.mentat_id,i))
        
class Box:
    
    def __init__(self):
        self.xlim = [0,np.inf]
        self.ylim = [0,0]
        self.zlim = [0,0]
        self.only = None
        
    def select(self,objects='Nodes',only=None,xlim=None,ylim=None,zlim=None,clear=False,reset=False):
        if xlim is not None: self.xlim = xlim
        if ylim is not None: self.ylim = ylim
        if zlim is not None: self.zlim = zlim
        if only is not None: self.only = only
        limits = *self.xlim, *self.ylim, *self.zlim
        
        if clear:
            self.clear()
        if reset:
            self.reset()
            
        if only is not None:
            pm.py_send('*select_filter_%s' % str(only).lower())
        
        pm.py_send('*select_method_box')
        pm.py_send('*select_%s %s %s %s %s %s %s' % (objects.lower(), *limits))
           
    def reset(self):
        pm.py_send('*select_reset')
         
    def clear(self,objects=''):
        if objects is not '':
            obj = '_'+objects
        else:
            obj = objects
        pm.py_send('*select_clear'+obj.lower())
        
    def select_x(self,objects='Nodes',y=0.0,z=0.0,only=None,clear=False,reset=False):
        self.xlim = [-np.inf,np.inf]
        self.ylim = [y,y]
        self.zlim = [z,z]
        if clear:
            self.clear()
        if reset:
            self.reset()
        self.select(objects,only=only)
        
    def select_y(self,objects='Nodes',x=0.0,z=0.0,only=None,clear=False,reset=False):
        self.ylim = [-np.inf,np.inf]
        self.xlim = [x,x]
        self.zlim = [z,z]
        if clear:
            self.clear()
        if reset:
            self.reset()
        self.select(objects,only=only)
        
    def select_z(self,objects='Nodes',x=0.0,y=0.0,only=None,clear=False,reset=False):
        self.zlim = [-np.inf,np.inf]
        self.xlim = [x,x]
        self.ylim = [y,y]
        if clear:
            self.clear()
        if reset:
            self.reset()
        self.select(objects,only=only)
        
    def select_xy(self,objects='Nodes',z=0.0,tol=1e-6,only=None,clear=False,reset=False):
        self.xlim = [-np.inf,np.inf]
        self.ylim = [-np.inf,np.inf]
        self.zlim = [z-tol,z+tol]
        if clear:
            self.clear()
        if reset:
            self.reset()
        self.select(objects,only=only)
        
    def select_yz(self,objects='Nodes',x=0.0,tol=1e-6,only=None,clear=False,reset=False):
        self.xlim = [x-tol,x+tol]
        self.ylim = [-np.inf,np.inf]
        self.zlim = [-np.inf,np.inf]
        if clear:
            self.clear()
        if reset:
            self.reset()
        self.select(objects,only=only)
        
    def select_zx(self,objects='Nodes',y=0.0,tol=1e-6,only=None,clear=False,reset=False):
        self.xlim = [-np.inf,np.inf]
        self.ylim = [y-tol,y+tol]
        self.zlim = [-np.inf,np.inf]
        if clear:
            self.clear()
        if reset:
            self.reset()
        self.select(objects,only=only)
        
class NextNodes:
    
    def __init__(self):
        self.nodes = 1
        self.PD = PointDistance()
        
    def _get_nset_entries(self):
        pm.py_send('*remove_sets ntemp')
        pm.py_send('*store_nodes ntemp all_selected')
        n = pm.py_get_int('nsets()')
        k = pm.py_get_int('nset_entries(%d)' % n)
        #pm.py_send('*remove_set_entries ntemp all_existing')
        
        return k
        
    def _get_set_entry_list(self,centroid,nnodes,extend,axes=[0,1,2],tol=1e-12):
        
        nodes = np.zeros(0,dtype=int)
        #coord = np.zeros((0,3))
        dist = np.zeros(0)
        
        n = pm.py_get_int('nsets()')
        k = pm.py_get_int('nset_entries(%d)' % n)
        
        #print('nsets, entries', n, k)
        
        for k in range(1,k+1):
            node = pm.py_get_int('set_entry(%d,%d)' %(n,k))
            nodes = np.append(nodes,node)

            x = pm.py_get_float('node_x(%d)' % node)
            y = pm.py_get_float('node_y(%d)' % node)
            z = pm.py_get_float('node_z(%d)' % node)
            xi = np.array([x,y,z])
            
            dist = np.append(dist, np.linalg.norm(centroid.take(axes)-xi.take(axes)))
            #coord = np.vstack((coord,[x,y,z]))
        
        sorted_nodes = nodes[np.argsort(dist)]
        sorted_dist = np.sort(dist)
        
        j = 0
        if extend:
            while (sorted_dist[nnodes+j]-sorted_dist[nnodes-1])**2<tol and nnodes+j < len(dist):
                j = j+1
        if j > 0:
            print('WARNING: Extended number of NextNodes from %d to %d due to equal distances.' % (nnodes,nnodes+j))
            
        return sorted_nodes[:nnodes+j]
        
    def select(self,centroid,nnodes,search_distance=1000,factor=0.5,
               increase=1.2,axes=[0,1,2],extend=False,
        	     only=None,clear=False,reset=False):
        
        pm.py_echo(0)
        di = search_distance
        ni = nnodes+1
        
        #n_tol = 50

        # shrink range to smaller limit
        #print('ni, nnodes, di', ni, nnodes, di)
        
        while factor <= 0.99:
        
            while ni > nnodes:
                self.PD.select(coordinates=np.array(centroid),distance=di,
                               only=only,clear=True,reset=True)
                ni = self._get_nset_entries()
                #print('search distance / number nodes / factor (loop):', di, ni, factor)
                if ni <= nnodes: # or ni <= n_tol
                    break
                else:
                    d = di
                    
                di = di*factor
            
            ni = nnodes+1
            di = d
        
            factor = factor*increase
                
                
        self.PD.select(coordinates=centroid,distance=d,
                       only=only,clear=True,reset=True)
        n = self._get_nset_entries()
        #print('search distance / number nodes:', d, n)
        
        nodes = self._get_set_entry_list(centroid,nnodes,extend,axes)
        pm.py_send('*remove_sets ntemp')
        nodelist = ' '.join(str(x) for x in nodes)
        
        pm.py_send('*select_clear_nodes')
        pm.py_send('*select_reset')
        pm.py_send('*select_nodes %s #' % nodelist)
        pm.py_echo(1)
        

class PointDistance:
    
    def __init__(self):
        self.distance = 0
        self.coordinates = [0,0,0]
        self.only = None
        
    def select(self,objects='Nodes',coordinates=None,distance=None,
               only=None,clear=False,reset=False):
        if distance is not None: self.distance = distance
        if coordinates is not None: self.coordinates = coordinates
        if only is not None: self.only = only
            
        x,y,z = self.coordinates
        
        if clear:
            self.clear()
        if reset:
            self.reset()
        
        pm.py_send('*select_method_point_dist')
        pm.py_send('*set_select_distance', str(self.distance))
        
        if only is not None:
            pm.py_send('*select_filter_%s' % str(only).lower())
        
        pm.py_send('*select_%s %s %s %s' % (objects.lower(),x,y,z))
           
    def reset(self):
        pm.py_send('*select_reset')
         
    def clear(self,objects=''):
        if objects is not '':
            obj = '_'+objects
        else:
            obj = objects
        pm.py_send('*select_clear'+obj.lower())