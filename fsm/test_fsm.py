#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 02:54:56 2020

@author: leij
"""

import random
from machine import Fsm

class Matter(object):
    pass

letter= Matter()
states=['A', 'B', 'C']

transitions = [
    { 'trigger': 'first', 'source': 'A', 'dest': 'B' },
    { 'trigger': 'second', 'source': 'A', 'dest': 'C' },
    { 'trigger': 'third', 'source': 'B', 'dest': 'C' },
]

# Initialize
machine = Fsm(letter, states=states, transitions=transitions, initial='A')
print(letter.state)
letter.second()
print(letter.state)
