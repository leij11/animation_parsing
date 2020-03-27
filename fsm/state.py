#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 14:36:18 2020

@author: leij
"""

from enum import Enum, EnumMeta

class State(object):
    """
    A class that manages of transitions
    that set assigned to the same trigger
    """
    dynamic_methods = ['on_enter', 'on_exit']

    def __init__(self, name, ignore_invalid_triggers=None):
        self._name = name
        self.ignore_invalid_triggers = ignore_invalid_triggers

    @property
    def name(self):
        if isinstance(self._name, Enum):
            return self._name.name
        else:
            return self._name

    @property
    def value(self):
        return self._name

    def __repr__(self):
        return "<%s('%s')@%s>" % (type(self).__name__, self.name, id(self))



