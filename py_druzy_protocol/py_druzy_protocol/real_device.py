#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
Created on 28 déc. 2015

@author: druzy
'''

from device import Renderer

class UpnpRenderer(Renderer):
    
    def __init__(self,client):
        Renderer.__init__(self,identifier=client.device.udn,protocol="upnp",name=client.device.get_friendly_name(),icon=client.device.icons[0]["url"])
        
        