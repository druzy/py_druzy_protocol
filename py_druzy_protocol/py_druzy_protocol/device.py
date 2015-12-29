#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 28 déc. 2015

@author: druzy
'''

from datetime import time
from py_druzy_mvc.model import Model

class Device(object):
    '''squelette d'un device'''
    
    def __init__(self,identifier,protocol,name,icon):
        object.__init__(self)
        
        self.identifier=identifier
        self.protocol=protocol
        self.name=name
        self.icon=icon
        
class Renderer(Device,Model):
    '''squelette d'un appareil de rendu'''
    
    PORT_FILE=18041
    
    def __init__(self,identifier,protocol,name,icon,duration=time(),time_position=time(),volume=100,volume_min=0,volume_max=100,mute=False):
        Device.__init__(self,identifier,protocol,name,icon)
        self.duration=duration
        self.time_position=time_position
        self.volume=volume
        self.volume_min=volume_min
        self.volume_max=volume_max
        
        