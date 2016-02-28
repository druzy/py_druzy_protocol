#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 28 déc. 2015

@author: druzy
'''

import os
from device import Renderer
import magic
from coherence.upnp.core import DIDLLite
from twisted.internet import defer

from py_druzy_server.restricted_server import RestrictedFileServer
 
class UpnpRenderer(Renderer):
    
    def __init__(self,device):
        
        Renderer.__init__(self,identifier=device.udn,protocol="upnp",name=device.get_friendly_name(),icon=device.icons[0]["url"])
        
        self.av_transport=device.get_client().av_transport
        self.rendering_control=device.get_client().rendering_control
        self.connection_manager=device.get_client().connection_manager
        self.av_transport_id=-1
        self.connection_id=0
        self.rcs_id=-1
        self.send_file=None
        self.err_send=None
        
        self._deferred_send=None
        
        
        print("avant send")
        self.send("/home/druzy/elliot.mp4")
        print("apres send")
        self.play()
        print("apres play")
        
    def send(self, f):
        self._deferred_send=self._send(f)
        return True
        
            
    @defer.inlineCallbacks
    def _send(self,f):
        protocols = (yield self.connection_manager.get_protocol_info())["Sink"]
        print(protocols)
        m=magic.open(magic.MIME_TYPE)
        m.load()
        mimetype=str(m.file(f))
        ask_protocol="http-get:*:"+mimetype+":*";
        if ask_protocol in protocols :
            ids= yield self.connection_manager.prepare_for_connection(ask_protocol,"/",-1,"Output")
            print(ids)
            self.connection_id=int(ids["ConnectionID"])
            self.rcs_id=int(ids["RcsID"])
            self.av_transport_id=int(ids["AVTransportID"])
            
            item=DIDLLite.classChooser(mimetype)(id=f,parentID=os.path.dirname(f),title=os.path.splitext(os.path.basename(f))[0],creator="pymita")
            
            #démarrage du serveur
            RestrictedFileServer(1532).add_file(f)
            yield self.av_transport.set_av_transport_uri(instance_id=self.av_transport_id,current_uri=RestrictedFileServer(1532).get_address(f))
            
            
    def play(self):
        self._deferred_send.addCallback(self._play)

    def _play(self,obj):
        self.av_transport.play(instance_id=self.av_transport_id)