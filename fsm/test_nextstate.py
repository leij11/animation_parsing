#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 20:58:32 2020

@author: leij
"""
import random
from machine import Fsm
states = ['A', 'C', 'B']
 # See the "alternative initialization" section for an explanation of the 1st argument to init
machine = Fsm(states=states, initial='A')
machine.add_ordered_transitions()
machine.next_state()
print(machine.state)
machine.next_state()
print(machine.state)