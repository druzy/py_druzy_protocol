#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 28 déc. 2015

@author: druzy
'''

from real_device import UpnpRenderer
from coherence.base import Coherence
from coherence.upnp.devices.control_point import ControlPoint
from twisted.internet import reactor
from threading import Timer,Thread

def get_discoverers():
    res=list()
    res.append(UpnpRendererDiscoverer())
    return res

    
class Discoverer(object):
    '''squelette d'un discoverer'''
    
    MEDIA_RENDERER_TYPE="urn:schemas-upnp-org:device:MediaRenderer"
    
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
        
    def start_discovery(self,delay=10,identifier=str(),device_discovery=None):
        '''voir Discoverer'''
        self._device_discovery=device_discovery
        config = {'logmode':'none'}
        c=Coherence(config)
        control=ControlPoint(c)
        control.connect(self.media_renderer_filter,"Coherence.UPnP.Device.detection_completed")
        #control.coherence.msearch.double_discover()
        Timer(delay,self.stop_discovery).start()
        Thread(None,reactor.run).start()
        
        
    def stop_discovery(self):
        '''voir Discoverer'''
        reactor.callFromThread(reactor.stop)
        
    def restart_discovery(self):
        self.stop_discovery()
        
        
    def media_renderer_filter(self,device):
        if Discoverer.MEDIA_RENDERER_TYPE in device.get_device_type():
            self._device_discovery(UpnpRenderer(device))
    
if __name__=="__main__":
    
    def coucou(device):
        print(device)
    
    renderer_list=get_discoverers()
    for renderer in renderer_list:
        renderer.start_discovery(device_discovery=coucou)

    