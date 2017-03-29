
import sys, os, math, random, functools

import numpy as np

import matplotlib
import matplotlib.pyplot as pp
import matplotlib.animation as anim

from IPython.display import display, HTML

class Turtle(object):
    deg = math.pi/180.0
    
    def __init__(self,terrarium,color='b'):
        # initialize state
        self.pos = (0,0)
        self.pen = True 
        self.angle = 0
        
        self.axes = terrarium.axes
        self.color = color
        
    def forward(self,distance):
        # compute new position
        posnew = (self.pos[0] + distance*math.cos(self.deg * self.angle),
                  self.pos[1] + distance*math.sin(self.deg * self.angle))
        
        # draw line if pen is down
        if self.pen:
            line2d = pp.Line2D((self.pos[0],posnew[0]),(self.pos[1],posnew[1]),color=self.color)
            self.axes.add_line(line2d) # 1
        
        self.pos = posnew

    def back(self,distance):
        self.forward(-distance)            
            
    def left(self,angle):
        # change state
         self.angle = (self.angle + angle) % 360.0

    def right(self,angle):
        # change state
         self.angle = (self.angle - angle) % 360.0
            
    def penup(self):
        # change state
        self.pen = False
    
    def pendown(self):
        # change state
        self.pen = True
    
    def point(self,width=2):
        circle = pp.Circle(self.pos,width,color=self.color)
        self.axes.add_patch(circle)
        
class animaxes(object):
    def __init__(self,fig,axes,duration=1):
        self.fig = fig
        self.axes = axes
        
        # grant access to true matplotlib axes to allow Terrarium.rescale()
        self.axis = axes.axis
        
        self.duration = duration        
        self.objects = []
    
    def add_line(self,line):
        self.axes.add_line(line)
        self.objects.append(line)
        
    def add_patch(self,patch):
        self.axes.add_patch(patch)
        self.objects.append(patch)
        
    def animate(self,i):
        for obj in self.objects[i*self.dt:(i+1)*self.dt]:
            if isinstance(obj,matplotlib.lines.Line2D):
                self.axes.add_line(obj)
            else:
                self.axes.add_patch(obj)
    
    def animation(self):
        self.dt = max(1,int(len(self.objects) / (self.duration * 30)))
        n = math.ceil(len(self.objects) / self.dt)        
        rate = self.duration * 1000 / n
        
        self.axes.clear()
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        for spine in ['bottom','top','left','right']:
            self.axes.spines[spine].set_color('0.9')
        
        return matplotlib.animation.FuncAnimation(self.fig,self.animate,blit=False,frames=n,interval=rate,repeat=False)    
    
class Terrarium(object):    
    def __init__(self,figsize=5,animate=False,duration=2): # by default, a little larger
        self.fig = pp.figure(figsize=(figsize,figsize))
        self.axes = pp.axes()
        
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        for spine in ['bottom','top','left','right']:
            self.axes.spines[spine].set_color('0.9')
        
        if animate:
            self.axes = animaxes(self.fig,self.axes,duration)

    def rescale(self):
        self.axes.axis('scaled')

        xmin, xmax, ymin, ymax = self.axes.axis()
        dx = (xmax - xmin) / 50
        self.axes.axis([xmin - dx,xmax + dx,ymin - dx,ymax + dx])
            
    def __enter__(self):
        return self
    
    def __exit__(self,*args):
        self.rescale()
        
        if isinstance(self.axes,animaxes):
            anim = self.axes.animation()
            display(HTML(anim.to_html5_video()))
            pp.close()