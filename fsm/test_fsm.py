import random
from machine import Fsm

states = ['A', 'C', 'B']
 # test ordered transitions
machine = Fsm(states=states, initial='A')
machine.add_ordered_transitions()
machine.next_state()
print(machine.state)
machine.next_state()
print(machine.state)

# test custome transitions
class Matter(object):
    pass

letter = Matter()
states = ['A', 'B', 'C']

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
print(machine.get_transitions())
