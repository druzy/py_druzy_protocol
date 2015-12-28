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
    
    def __init__(self,identifier,protocol,name,icon,duration=time(),timePosition=time(),volume=100,volumeMin=0,volumeMax=100,mute=False):
        Device.__init__(self,identifier,protocol,name,icon)
        self.duration=duration
        self.timePosition=timePosition
        self.volume=volume
        self.volumeMin=volumeMin
        self.volumeMax=volumeMax
        
        