#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
Created on 28 déc. 2015

@author: druzy
'''

from device import Renderer

class UpnpRenderer(Renderer):
    
    def __init__(self,device):
        Renderer.__init__(self,identifier=device.udn,protocol="upnp",name=device.get_friendly_name(),icon=device.icons[0]["url"])
        
        