# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:05:55 2019

@author: dutzi
"""


import numpy as np
import py_post as po
from .node import Node
import time

import matplotlib.pyplot as plt

class PostFile:
    
    def __init__(self, filename, job=''):
        self.job = job
        if filename[-4:] == '.t16':
            self.filename = filename
        else:
            self.filename = '.'.join(filename.split('.')[:-1])+'_'+self.job.label+'.t16'

    def __enter__(self):
        self.p = po.post_open(self.filename)
        self.nincs = self.p.increments()
        
        try:
            self.p.moveto(1)
        except:
            raise TypeError('Error opening post file: ',self.filename)
            
        self.time = np.zeros(self.nincs-1)
        for n in range(self.nincs-1):
            self.p.moveto(n+1)
            self.time[n] = self.p.time
            
        self.ConnectivityMatrix = ConnectivityMatrix(self)
        
        self.global_value_labels = []
        for i in range(self.p.global_values()):
            self.global_value_labels.append(self.p.global_value_label(i))
            
        self.node_scalar_labels = []
        for i in range(self.p.node_scalars()):
            self.node_scalar_labels.append(self.p.node_scalar_label(i))
            
        self.element_scalar_labels = []
        for i in range(self.p.element_scalars()):
            self.element_scalar_labels.append(self.p.element_scalar_label(i))
            
        self.HistoryPlot = HistoryPlot(self)
            
        return self
        
    def __exit__(self, H_type, H_value, H_traceback):
        self.p.close()
        
class ConnectivityMatrix:
    
    def __init__(self,postfile):
        self.pf = postfile
        self.nnodes = self.pf.p.nodes()
        self.nelems = self.pf.p.elements()
        # max. nodes per element = 20 !! (hardcoded)
        # 1st column = element ids
        # rows ... connected nodes per element.id
        self.connectivity = -1*np.zeros((self.nelems,1+20),dtype=int)
        
        # store current time for time measurement
        clock0_build = time.clock()
        time0_build = time.time()
        
        for i in range(self.nelems):
            element = self.pf.p.element(i)
            self.connectivity[i,0] = self.pf.p.element_id(i)
            self.connectivity[i,1:element.len+1] = element.items

        clock1_build = time.clock()
        time1_build = time.time()

        time_dclock_build = clock1_build - clock0_build
        time_dtime_build  = time1_build  - time0_build
        print(r'\pagebreak')
        print(' ')
        print('\n## Generation of Connectivity Matrix')
        print('Time measurement for execution times .\n')
        print('    total  cpu time "connectivity build": {:10.3f} seconds'.format(time_dclock_build))
        print('    total wall time "connectivity build": {:10.3f} seconds\n'.format(time_dtime_build))
        

    def elements_at_node(self,node_id):
        i,j = np.where(self.connectivity[:,1:]==node_id)
        
        # i = [element.id=1, 1,2,3,4,nan]
        # k = [element.id=1, 1,2,3,4] (list contains no nan entries)
        k = i[np.where(i>=0)]
        return self.connectivity[:,0].take(np.unique(k))
        
    def element_scalar_at_node(self,scalar_index,node_id):
        elements = self.elements_at_node(node_id)
        scalar = np.zeros(len(elements))
        for i,e in enumerate(elements):
            slist = self.pf.p.element_scalar(self.pf.p.element_sequence(e),scalar_index)
            for s in slist:
                #print(i,slist)
                if s.id == node_id:
                    scalar[i] = s.value
        return np.mean(scalar)
        
class HistoryPlot:
    
    def __init__(self,postfile):
        self.pf = postfile
        self.fig = plt.figure(1)
        self.ax = self.fig.add_subplot(111)
        plt.close(self.fig)
        self.history_data = []
    
    def add(self,x,y,nodes,increments=None,show=True,reset=False,legend='inside'):
        
        # reset history plot
        if reset: self.clear()
        
        # check if nodes are passed in format [n1,[n2]] or [n1,n2]
        # if [n1,n2] then change to [n1,[n2]]
        if type(nodes[1]) == int:
            nodes = [nodes[0],[nodes[1]]]
        self.nodes = nodes
        
        # select all increments if no increments are passed (=False)
        if increments is None:
            self.increments = np.arange(self.pf.p.increments()-1)
        else:
            self.increments = np.array(increments)
        
        # check if x-node is passed as number or node object
        if isinstance(self.nodes[0],Node):
            self.node_x = nodes[0].mentat_id
        else:
            self.node_x = nodes[0]
            
        # check if y-nodes are passed as numbers or node objects
        if isinstance(self.nodes[1][0],Node):
            self.nodes = [n.mentat_id for n in self.nodes[1]]
        else:
            self.nodes = nodes[1]
        
        # init data with zeros
        self.data = np.zeros((len(self.increments),len(self.nodes)+1))
        
        # check if x-label is node-based
        if 'Displacement' in x or 'Force' in x or 'Moment' in x or 'Rotation' in x:
            self.i = self.pf.node_scalar_labels.index(x)
            xtype = 'node'
        else: # element based x-label
            self.i = self.pf.element_scalar_labels.index(x)
            xtype = 'element'
        
        # check if y-label is node-based
        if 'Displacement' in y or 'Force' in y or 'Moment' in y or 'Rotation' in y:
            self.j = self.pf.node_scalar_labels.index(y)
            ytype = 'node'
        else: # element based y-label
            self.j = self.pf.element_scalar_labels.index(y)
            ytype = 'element'
        
        # loop over increments
        for k,inc in enumerate(self.increments):
            self.pf.p.moveto(inc+1)
            #nx = self.pf.p.node_id(node_x)
            
            # check if x-label is node-based
            if xtype == 'node': # check if node exists in postfile
                if self.pf.p.node_sequence(self.node_x) == -1:
                        raise ValueError('Node %d not found!' % self.node_x)
                self.data[k,0] = self.pf.p.node_scalar(self.pf.p.node_sequence(self.node_x), self.i)
            else: # get all connected elements and extract nodal value
                element_scalar_at_node = self.pf.ConnectivityMatrix.element_scalar_at_node
                self.data[k,0] = element_scalar_at_node(self.i, self.node_x)
            
            # loop over y-nodes
            for l,n in enumerate(self.nodes):
                #ny = self.pf.p.node_id(n)
                
                # check if y-label is node-based
                if ytype == 'node': # check if node exists in postfile
                    if self.pf.p.node_sequence(n) == -1:
                        raise ValueError('Node %d not found!' % n)
                    self.data[k,l+1] = self.pf.p.node_scalar(self.pf.p.node_sequence(n), self.j)
                else: # get all connected elements and extract nodal value
                    element_scalar_at_node = self.pf.ConnectivityMatrix.element_scalar_at_node
                    self.data[k,l+1] = element_scalar_at_node(self.j, n)
                    
        # check if all data-values are close to 0 for the 1st increment
        # e.q. set 1.4546e-12 to 0.0
        if np.allclose(self.data[0],0):
            self.data[0] = 0.0
        
        # plot curves
        for k,curve in enumerate(self.data.T[1:]):
            lbl = 'Node '+str(self.nodes[k])
            #lbl_full = x+' '+lbl
            self.ax.plot(self.data[:,0],curve,'.-',label=lbl)
        
        # set x-label
        self.ax.set_xlabel(x+' (Node '+str(self.node_x)+')')
        
        # set y-label with node if one node was passed
        if len(self.nodes) == 1 and len(self.ax.lines) == 1:
            self.ax.set_ylabel(y+' (Node '+str(self.nodes[0])+')')
        else: # set y-label without node if more nodes were passed
        
            # check if curves have different ylabels --> remove ylabel
            if not reset and self.y != y:

                for line in self.ax.lines[:-len(self.nodes)]:
                    if '(' not in line.get_label():
                        line.set_label(self.y+' ('+line.get_label()+')')
                for line in self.ax.lines[-len(self.nodes):]:
                    line.set_label(y+' ('+line.get_label()+')')
                
                self.ax.set_ylabel('')    
                self.y = ''
            else:
                self.ax.set_ylabel(y)
            
            # show legend #loc='best'
            if legend == 'inside':
                self.lgd = self.ax.legend(loc='best')
            else:
                self.lgd = self.ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
            
        # store x,y labels
        self.x = x
        self.y = y
            
        # enable grid
        self.ax.grid()
        # show plot
        if show: self.show()
            
        self.history_data.append(self.data)
            
        # fill with nan's
        #np.pad(np.array([1,2,3.3]),(0,5),'constant',constant_values=(np.nan,np.nan))
        
        return self.data, self.fig, self.ax
        
    def savefig(self,ftype='.pdf'):
        fx = self.x.replace(' ', '')
        fy = self.y.replace(' ', '')
        nx = 'N'+str(self.node_x)
        ny = '-'.join('N'+str(n) for n in self.nodes)
        
        sdir = '\\'.join(self.pf.filename.split('\\')[:-1])
        sname = sdir+'\\'+fx+'-'+nx+'_'+fy+'-'+ny+ftype
        
        try:
            self.fig.savefig(sname,dpi=300,bbox_extra_artists=(self.lgd,),bbox_inches='tight')
        except:
            self.fig.savefig(sname,dpi=300)
    
    def savedata(self,ftype='.csv'):
        fx = self.x.replace(' ', '')
        fy = self.y.replace(' ', '')
        nx = 'N'+str(self.node_x)
        ny = '-'.join('N'+str(n) for n in self.nodes)
        
        sdir = '\\'.join(self.pf.filename.split('\\')[:-1])
        name = sdir+'\\'+fx+'-'+nx+'_'+fy+'-'+ny
        
        for i,hd in enumerate(self.history_data):
            np.savetxt(name+'_'+str(i)+ftype,hd,delimiter=', ')
        
    def clear(self):
        self.ax.clear()
        self.history_data = []
        
    def show(self):
        dummy = plt.figure()
        new_manager = dummy.canvas.manager
        new_manager.canvas.figure = self.fig
        self.fig.set_canvas(new_manager.canvas)
        #plt.show()