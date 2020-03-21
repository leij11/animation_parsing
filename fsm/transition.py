#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 14:37:27 2020

@author: leij
"""
from enum import Enum, EnumMeta
    
class Transition(object):


    def __init__(self, source, dest):

        self.source = source
        self.dest = dest

    def execute(self, event_data):
        fsm = event_data.fsm


        if self.dest:  
            self._change_state(event_data)


    def _change_state(self, event_data):
        event_data.fsm.get_state(self.source).exit(event_data)
        event_data.fsm.set_state(self.dest, event_data.model)
        event_data.update(getattr(event_data.model, event_data.fsm.model_attribute))
        event_data.fsm.get_state(self.dest).enter(event_data)


    def __repr__(self):
        return "<%s('%s', '%s')@%s>" % (type(self).__name__,
                                        self.source, self.dest, id(self))