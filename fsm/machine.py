#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 14:27:15 2020

@author: leij
"""

from state import State
from transition import Transition
from action import Action
from collections import OrderedDict, defaultdict, deque
from functools import partial
from six import string_types
from builtins import object
from enum import Enum, EnumMeta


def to_list(obj):
    """
    A method that converts any type of object into list
    For example, none is empty list[]
                 tuple (a,b) is list [1,2]
    ...

   Parameters
    ----------
    obj : 
        Item that is going to parse into list format


   Returns
    -------
    list that contains the object
    """
    if obj is not None:
        if isinstance(obj, (list, tuple, EnumMeta)):
            return obj
        else:
            return [obj]

    return []

#print(to_list((1,2)))


def _get_trigger(model, fsm, trigger_name, *args, **kwargs):
    try:
        event = fsm.events[trigger_name]
    except KeyError:
        raise AttributeError("Do not know event named '%s'." % trigger_name)
    return event.trigger(model, *args, **kwargs)


def _prep_ordered_arg(desired_length, arguments=None):
    """Ensure list of arguments passed to add_ordered_transitions has the proper length.
    """
    arguments = to_list(arguments) if arguments is not None else [None]
    if len(arguments) != desired_length and len(arguments) != 1:
        raise ValueError("Argument length must be either 1 or the same length as "
                         "the number of transitions.")
    if len(arguments) == 1:
        return arguments * desired_length
    return arguments

class Fsm(object):

    separator = '_'  # separates callback type from state/transition name
    wildcard_all = '*'  # will be expanded to ALL states
    wildcard_same = '='  # will be expanded to source state
    state_cls = State
    transition_cls = Transition
    event_cls = Action

    def __init__(self, model='self', states=None, initial='initial', transitions=None,
                 send_event=False, auto_transitions=True,
                 ordered_transitions=False, ignore_invalid_triggers=None,
                 before_state_change=None, after_state_change=None, name=None,
                 queued=False, prepare_event=None, finalize_event=None, model_attribute='state', **kwargs):
        try:
            super(Fsm, self).__init__(**kwargs)
        except TypeError as err:
            raise ValueError('Passing arguments {0} caused an inheritance error: {1}'.format(kwargs.keys(), err))

        # initialize protected attributes first
        self._queued = queued
        self._transition_queue = deque()
        self._before_state_change = []
        self._after_state_change = []
        self._prepare_event = []
        self._finalize_event = []
        self._initial = None

        self.states = OrderedDict()
        self.events = {}
        self.send_event = send_event
        self.auto_transitions = auto_transitions
        self.ignore_invalid_triggers = ignore_invalid_triggers
        self.prepare_event = prepare_event
        self.before_state_change = before_state_change
        self.after_state_change = after_state_change
        self.finalize_event = finalize_event
        self.name = name + ": " if name is not None else ""
        self.model_attribute = model_attribute

        self.models = []

        if states is not None:
            self.add_states(states)

        if initial is not None:
            self.initial = initial

        if transitions is not None:
            self.add_transitions(transitions)

        if ordered_transitions:
            self.add_ordered_transitions()

        if model:
            self.add_model(model)

    def add_model(self, model, initial=None):
        models = to_list(model)

        if initial is None:
            if self.initial is None:
                raise ValueError("No initial state configured for machine, must specify when adding model.")
            else:
                initial = self.initial

        for mod in models:
            mod = self if mod == 'self' else mod
            if mod not in self.models:
                self._checked_assignment(mod, 'trigger', partial(_get_trigger, mod, self))

                for trigger, _ in self.events.items():
                    self._add_trigger_to_model(trigger, mod)

                for _, state in self.states.items():
                    self._add_model_to_state(state, mod)

                self.set_state(initial, model=mod)
                self.models.append(mod)


    @classmethod
    def _create_transition(cls, *args, **kwargs):
        return cls.transition_cls(*args, **kwargs)

    @classmethod
    def _create_event(cls, *args, **kwargs):
        return cls.event_cls(*args, **kwargs)

    @classmethod
    def _create_state(cls, *args, **kwargs):
        return cls.state_cls(*args, **kwargs)

    @property
    def initial(self):
        """ Return the initial state. """
        return self._initial

    @initial.setter
    def initial(self, value):
        if isinstance(value, State):
            if value.name not in self.states:
                self.add_state(value)
            else:
                assert self._has_state(value)
            self._initial = value.name
        else:
            state_name = value.name if isinstance(value, Enum) else value
            if state_name not in self.states:
                self.add_state(state_name)
            self._initial = state_name



    @property
    def model(self):
        if len(self.models) == 1:
            return self.models[0]
        return self.models

    @property
    def finalize_event(self):
        return self._finalize_event

    # this should make sure that finalize_event is always a list
    @finalize_event.setter
    def finalize_event(self, value):
        self._finalize_event = to_list(value)

    def get_state(self, state):
        if isinstance(state, Enum):
            state = state.name
        if state not in self.states:
            raise ValueError("State '%s' is not a registered state." % state)
        return self.states[state]


    def is_state(self, state, model):
        return getattr(model, self.model_attribute) == state

    def get_model_state(self, model):
        return self.get_state(getattr(model, self.model_attribute))

    def set_state(self, state, model=None):
        state = self.get_state(state)
        models = self.models if model is None else to_list(model)

        for mod in models:
            setattr(mod, self.model_attribute, state.value)

    def add_state(self, *args, **kwargs):
        """ Alias for add_states. """
        self.add_states(*args, **kwargs)

    def add_states(self, states, on_enter=None, on_exit=None,
                   ignore_invalid_triggers=None, **kwargs):
        ignore = ignore_invalid_triggers
        if ignore is None:
            ignore = self.ignore_invalid_triggers

        states = to_list(states)

        for state in states:
            if isinstance(state, (string_types, Enum)):
                state = self._create_state(
                    state, on_enter=on_enter, on_exit=on_exit,
                    ignore_invalid_triggers=ignore, **kwargs)
            elif isinstance(state, dict):
                if 'ignore_invalid_triggers' not in state:
                    state['ignore_invalid_triggers'] = ignore
                state = self._create_state(**state)
            self.states[state.name] = state
            for model in self.models:
                self._add_model_to_state(state, model)
        # Add automatic transitions after all states have been created
        if self.auto_transitions:
            for state in self.states.keys():
                self.add_transition('to_%s' % state, self.wildcard_all, state)

    def _add_model_to_state(self, state, model):
        self._checked_assignment(model, 'is_%s' % state.name, partial(self.is_state, state.value, model))
        for callback in self.state_cls.dynamic_methods:
            method = "{0}_{1}".format(callback, state.name)
            if hasattr(model, method) and inspect.ismethod(getattr(model, method)) and \
                    method not in getattr(state, callback):
                state.add_callback(callback[3:], method)

    def _checked_assignment(self, model, name, func):
        if hasattr(model, name):
            print("Model already contains an attribute")
        else:
            setattr(model, name, func)

    def _add_trigger_to_model(self, trigger, model):
        self._checked_assignment(model, trigger, partial(self.events[trigger].trigger, model))

    def get_triggers(self, *args):
        states = set(args)
        return [t for (t, ev) in self.events.items() if any(state in ev.transitions for state in states)]

    def add_transition(self, trigger, source, dest,  **kwargs):

        if trigger == self.model_attribute:
            raise ValueError("Trigger name cannot be same as model attribute name.")
        if trigger not in self.events:
            self.events[trigger] = self._create_event(trigger, self)
            for model in self.models:
                self._add_trigger_to_model(trigger, model)

        if source == self.wildcard_all:
            source = list(self.states.keys())
        else:
            source = [s.name if self._has_state(s) or isinstance(s, Enum) else s for s in to_list(source)]

        for state in source:
            _dest = state if dest == self.wildcard_same else dest
            if _dest and self._has_state(_dest) or isinstance(_dest, Enum):
                _dest = _dest.name
            _trans = self._create_transition(state, _dest, **kwargs)
            self.events[trigger].add_transition(_trans)

    def add_transitions(self, transitions):

        for trans in to_list(transitions):
            if isinstance(trans, list):
                self.add_transition(*trans)
            else:
                self.add_transition(**trans)

    def add_ordered_transitions(self, states=None, trigger='next_state',
                                loop=True, loop_includes_initial=True,
                                 **kwargs):

        if states is None:
            states = list(self.states.keys())  # need to listify for Python3
        len_transitions = len(states)
        if len_transitions < 2:
            raise ValueError("Can't create ordered transitions on a Machine "
                             "with fewer than 2 states.")
        if not loop:
            len_transitions -= 1
        # ensure all args are the proper length
      #  conditions = _prep_ordered_arg(len_transitions, conditions)
       # unless = _prep_ordered_arg(len_transitions, unless)
       # before = _prep_ordered_arg(len_transitions, before)
       # after = _prep_ordered_arg(len_transitions, after)
       # prepare = _prep_ordered_arg(len_transitions, prepare)
        # reorder list so that the initial state is actually the first one
        idx = states.index(self._initial)
        states = states[idx:] + states[:idx]

        for i in range(0, len(states) - 1):
            self.add_transition(trigger, states[i], states[i + 1],
                             #   conditions=conditions[i],
                              #  unless=unless[i],
                               # before=before[i],
                                #after=after[i],
                                #prepare=prepare[i],
                                **kwargs)
        if loop:
            self.add_transition(trigger, states[-1],
                                # omit initial if not loop_includes_initial
                                states[0 if loop_includes_initial else 1],
                                **kwargs)

    def get_transitions(self, trigger="", source="*", dest="*"):
        if trigger:
            events = (self.events[trigger], )
        else:
            events = self.events.values()
        transitions = []
        for event in events:
            transitions.extend(
                itertools.chain.from_iterable(event.transitions.values()))
        return [transition
                for transition in transitions
                if (transition.source, transition.dest) == (
                    source if source != "*" else transition.source,
                    dest if dest != "*" else transition.dest)]


    def dispatch(self, trigger, *args, **kwargs):

        return all([getattr(model, trigger)(*args, **kwargs) for model in self.models])


    def _has_state(self, state):
        if isinstance(state, State):
            if state in self.states.values():
                return True
            else:
                raise ValueError('State %s has not been added to the fsm' % state.name)
        else:
            return False

    def _process(self, trigger):
        # process queued events
        self._transition_queue.append(trigger)
        if len(self._transition_queue) > 1:
            return True

        while self._transition_queue:
            try:
                self._transition_queue[0]()
                self._transition_queue.popleft()
            except Exception:
                self._transition_queue.clear()
                raise
        return True


 
