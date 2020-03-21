#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 14:36:18 2020

@author: leij
"""

from enum import Enum, EnumMeta

class State(object):
    dynamic_methods = ['on_enter', 'on_exit']

    def __init__(self, name, on_enter=None, on_exit=None,
                 ignore_invalid_triggers=None):
        self._name = name
        self.ignore_invalid_triggers = ignore_invalid_triggers
        self.on_enter = listify(on_enter) if on_enter else []
        self.on_exit = listify(on_exit) if on_exit else []

    @property
    def name(self):
        if isinstance(self._name, Enum):
            return self._name.name
        else:
            return self._name

    @property
    def value(self):
        return self._name

    def enter(self, event_data):
        for handle in self.on_enter:
            event_data.machine.callback(handle, event_data)

    def exit(self, event_data):
        for handle in self.on_exit:
            event_data.machine.callback(handle, event_data)


    def __repr__(self):
        return "<%s('%s')@%s>" % (type(self).__name__, self.name, id(self))



