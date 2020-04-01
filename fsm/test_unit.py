#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from machine import*
import unittest

class fsmTest(unittest.TestCase):

 
    def test_States_1(self):
        states=['A','C','B']
        m=Fsm(states=states, initial='A')
        self.assertEqual(m.state,'A')
        m=Fsm(states=states, initial='C')
        self.assertEqual(m.state,'C')

    def test_States_2(self):
        states=['A','C','B']
        m=Fsm(states=states, initial='C')
        self.assertEqual(m.state,'C')
    
    def test_Transition_1(self):
        #user define states
        states = ['0', '1']
        transitions = [
            { 'trigger': 'a', 'source': '0', 'dest': '1' },
            { 'trigger': 'b', 'source': '1', 'dest': '0' },]
        m = Fsm(states=states, transitions=transitions, initial='0')
        m.a()
        self.assertEquals(m.state,'1')
    
    def test_Transition_2(self):
        #user define states
        states = ['0', '1', '2', '3', '4', '5']
        
        #user define transitions
        transitions = [
            { 'trigger': 'a', 'source': '0', 'dest': '1' },
            { 'trigger': 'b', 'source': '1', 'dest': '2' },
            { 'trigger': 'c', 'source': '1', 'dest': '3' },
            { 'trigger': 'd', 'source': '0', 'dest': '4' },
            { 'trigger': 'e', 'source': '4', 'dest': '5' },
        ]
        m = Fsm(states=states, transitions=transitions, initial='1')
        m.b()
        self.assertEquals(m.state,'2')




if __name__ == "__main__":
    unittest.main()