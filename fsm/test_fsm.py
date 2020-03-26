from machine import Fsm

class Things(object):
    pass

day = Things()

letter = Matter()
states = ['School', 'Home', 'Company','Club']

transitions = [
    { 'trigger': 'Rest', 'source': 'School', 'dest': 'Home' },
    { 'trigger': 'Study', 'source': 'Home', 'dest': 'School' },
    { 'trigger': 'work', 'source': 'Home', 'dest': 'Company' },
    { 'trigger': 'Play', 'source': 'Home', 'dest': 'Club' },
    { 'trigger': 'Rest', 'source': 'Company', 'dest': 'Home' },
    { 'trigger': 'Sleep', 'source': 'Club', 'dest': 'Home' },
    { 'trigger': 'Finish', 'source': 'School', 'dest': 'f' },
    { 'trigger': 'Finish', 'source': 'Company', 'dest': 'f' },
]
machine = Fsm(day, states=states, transitions=transitions, initial='Home')
#Initial State
print(day.state)
#From home to school
day.Study()
print(day.state)
#From school to home
day.Rest()
print(day.state)
