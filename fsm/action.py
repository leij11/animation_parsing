#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 14:38:48 2020
@author: leij11
"""
from collections import OrderedDict, defaultdict, deque
from functools import partial
from state import State
class Action(object):
    """
    A class that manages of transitions
    that set assigned to the same trigger
    """
    def __init__(self, name, fsm):
        self.name = name
        self.fsm = fsm
        self.transitions = defaultdict(list)

    def add_transition(self, transition):
        self.transitions[transition.source].append(transition)

    def trigger(self, model, *args, **kwargs):
        func = partial(self._trigger, model, *args, **kwargs)
        return self.fsm._process(func)

    def _trigger(self, model, *args, **kwargs):
        state = self.fsm.get_model_state(model)
        if state.name not in self.transitions:
            msg = "%sCan't trigger event %s from state %s!" % (self.fsm.name, self.name,
                                                               state.name)
            ignore = state.ignore_invalid_triggers if state.ignore_invalid_triggers is not None \
                else self.fsm.ignore_invalid_triggers
            if ignore:
                return False
            else:
                raise Exception('Machine Error: '+msg)
        event_data = Helper(state, self, self.fsm, model, args=args, kwargs=kwargs)
        return self._process(event_data)

    def _process(self, event_data):

        try:
            for trans in self.transitions[event_data.state.name]:
                event_data.transition = trans
                if trans.execute(event_data):
                    event_data.result = True
                    break
        except Exception as err:
            event_data.error = err
            raise
        return event_data.result

    def __repr__(self):
        return "<%s('%s')@%s>" % (type(self).__name__, self.name, id(self))

class Helper(object):
    def __init__(self, state, event, fsm, model, args, kwargs):
        self.state = state
        self.event = event
        self.fsm = fsm
        self.model = model
        self.args = args
        self.kwargs = kwargs
        self.transition = None
        self.error = None
        self.result = False
    def update(self, state):

        if not isinstance(state, State):
            self.state = self.fsm.get_state(state)

    def __repr__(self):
        return "<%s('%s', %s)@%s>" % (type(self).__name__, self.state,
                                      getattr(self, 'transition'), id(self))