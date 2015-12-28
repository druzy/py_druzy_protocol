#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 28 déc. 2015

@author: druzy
'''

from coherence.base import Coherence
from coherence.upnp.devices.control_point import ControlPoint
import threading
from twisted.internet import reactor

def get_discoverers():
    '''renvoie les discoverers de ce module différent de Discoverer'''
    pass
    
class Discoverer(object):
    '''squelette d'un discoverer'''
    
    def __init__(self):
        object.__init__(self)
        
    def start_discovery(self,delay=10,identifier=str(),device_discovery=lambda :()):
        '''démarre la découverte de service
        doit être overrided
        
        delay : le temps que dure la découverte
        device_discovery : fonction appelé après la découverte du service
        '''
        pass
        
    def stop_discovery(self):
        ''' stop la découverte de service
        must be overrided
        '''
        pass
    
    def restart_discovery(self):
        '''redémarre la découverte de service
        must be overrided
        '''
        
        self.stop_discovery()
        
class UpnpRendererDiscoverer(Discoverer):
    
    def __init__(self):
        Discoverer.__init__(self)
        
    def start_discoverer(self,device_discover=lambda:()):
        cp = ControlPoint(Coherence({'logmode':'warning'}),auto_client=['MediaRenderer'])
        cp.connect(self._media_renderer_found, 'Coherence.UPnP.ControlPoint.MediaRenderer.detected')
        cp.connect(self._media_renderer_removed, 'Coherence.UPnP.ControlPoint.MediaRenderer.removed')
        
        
    def _media_renderer_found(self,client,udn):
        print("media_renderer_found", client)
        print("media_renderer_found", client.device.get_friendly_name())
     
    def _media_renderer_removed(self,udn):
        print("media_renderer_removed", udn)
        
if __name__=="__main__":
    u=UpnpRendererDiscoverer()
    
    reactor.callWhenRunning(u.start_discoverer)
    reactor.run()
