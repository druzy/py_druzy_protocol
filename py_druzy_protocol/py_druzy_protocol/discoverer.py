#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 28 déc. 2015

@author: druzy
'''

from twisted.internet import reactor
from coherence.base import Coherence
from coherence.upnp.devices.control_point import ControlPoint
from real_device import UpnpRenderer
from threading import Timer,Thread

def get_discoverers():
    res=list()
    res.append(UpnpRendererDiscoverer())
    return res

    
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
    '''représente un découvreur de renderer UPNP'''
    
    
    def __init__(self):
        Discoverer.__init__(self)
        
    def start_discovery(self,delay=10,identifier=str(),device_discovery=lambda :()):
        '''voir Discoverer'''
        self._device_discovery=device_discovery
        reactor.callWhenRunning(self._start)
        Timer(10,self.stop_discovery).start()
        Thread(None,reactor.run).start()
        
    
    def stop_discovery(self):
        '''voir Discoverer'''
        reactor.callFromThread(reactor.stop)
    
    def _start(self):
        cp = ControlPoint(Coherence({'logmode':'warning', 'port':'12345'}))
        cp.connect(self._media_renderer_found, 'Coherence.UPnP.ControlPoint.MediaRenderer.detected')
             
    def _media_renderer_found(self,client,udn):
        #print("media_renderer_found", udn)
        #print("client.device.__dict__ : ", client.device.__dict__)
        self._device_discovery(UpnpRenderer(client))
        
    
    def _media_renderer_removed(self,udn):
        #print("media_renderer_removed", udn)
        pass



if __name__=="__main__":
    
    def coucou(device):
        print(device)
    
    renderer_list=get_discoverers()
    for renderer in renderer_list:
        renderer.start_discovery(device_discovery=coucou)

    