"""
Author:     Chris Knowles
Date:       Oct 2018
Copyright:  University of Sunderland, (c) 2018
File:       exceptions.py
Version:    1.0.0
Notes:      Digital version of the 'Turn Or Burn' PnP board game from Interformic Game (https://interformic.com/torb/)
                - Set of exception classes associated with the FSM
"""

# Imports
# Consts
# Globals
# Functions


# Classes
class GuardFailedException(Exception):
    def __init__(self, source_state, target_state, transition):
        msg = "Guard function failed during transition between states [{0}]:[{1}]->[{2}]:[{3}] \
using transition [{4}]".format(source_state.uid, source_state.name, target_state.uid, target_state.name, transition.uid)
        super().__init__(msg)
        self._source_state = source_state
        self._target_state = target_state
        self._transition = transition

    @property
    def source_state(self):
        return self._source_state

    @property
    def target_state(self):
        return self._target_state

    @property
    def transition(self):
        return self._transition


class StateNotFoundError(Exception):
    def __init__(self, state, transition):
        msg = "State [{0}]:[{1}] not found in transition [{2}]".format(state.uid, state.name, transition.uid)
        super().__init__(msg)
        self._state = state
        self._transition = transition

    @property
    def state(self):
        return self._state

    @property
    def transition(self):
        return self._transition


class NoTransitionsError(Exception):
    def __init__(self, state):
        msg = "State [{0}]:[{1}] has no transitions".format(state.uid, state.name)
        super().__init__(msg)
        self._state = state

    @property
    def state(self):
        return self._state


class TransitionNotFoundError(Exception):
    def __init__(self, state0, state1):
        msg = "Transition not found that has states [{0}]:[{1}]->[{2}]:[{3}]".format(state0.uid, state0.name,
                                                                                     state1.uid, state1.name)
        super().__init__(msg)
        self._state0 = state0
        self._state1 = state1

    @property
    def state0(self):
        return self._state0

    @property
    def state1(self):
        return self._state1


class DuplicateTransitionError(Exception):
    def __init__(self, state0, state1):
        msg = "Transition is duplicate with states [{0}]:[{1}]->[{2}]:[{3}]".format(state0.uid, state0.name,
                                                                                    state1.uid, state1.name)
        super().__init__(msg)
        self._state0 = state0
        self._state1 = state1

    @property
    def state0(self):
        return self._state0

    @property
    def state1(self):
        return self._state1
