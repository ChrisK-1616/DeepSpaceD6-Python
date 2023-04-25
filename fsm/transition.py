"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       transition.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - Transition class that represents a FSM transition between application states
"""

# Imports
from data_model.identified_entity import IdentifiedEntity
from fsm.exceptions import GuardFailedException


# Consts
# Globals
# Functions


# Classes
class Transition(IdentifiedEntity):
    def __init__(self, source, target, guard=None):
        """
        Initialiser for the Transition class

        :attr _source: source state of the transition, NOTE: the source state of the transition should NOT change as
                       this will be the state that 'owns' this transition and integrity of such a relationship MUST be
                       maintained, it can be read

        :attr _target: target state of the transition,  NOTE: the target state of the transition should NOT change as
                       this will potentially break the set exclusivity of the transition within the state that 'owns'
                       this transition and integrity of such a relationship MUST be maintained, it can be read

        :attr _guard: function to call when the transition is 'fired' to check if any guard conditions have been met,
                      this guard function must have a signature that receives a source state and a target state, these
                      states can then be utilised in the operation of the guard, use None if no guard needs to be
                      checked for this transition

        :param source: fsm.state.State object at the source 'end' of this transition
        :param target: fsm.state.State object at the target 'end' of this transition
        :param guard: function object that acts as a guard for this transition
        """
        super().__init__()
        self._source = source
        self._target = target
        self._guard = guard

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def guard(self):
        return self._guard

    @guard.setter
    def guard(self, guard):
        self._guard = guard

    def __eq__(self, other):
        """
        Equality predicate method to check this transition against another supplied transition, it is equality if this
        transition has the same states in its states list as the supplied other transition

        :param other: fsm.state.Transition object to check equality with

        :return boolean: return True if transition objects evaluate to equal, otherwise return False
        """
        return (self.source == other.source) and (self.target == other.target)

    def __str__(self):
        """
        String representation of a fsm.transition.Transition object

        :return string: string representation
        """
        return "transition [{0}]:{1}->{2}".format(self.uid, self.source, self.target)

    def fire(self, one_off_guard=None, apply_short_circuit=True):
        """
        Call this method to 'fire' the transition, this will move from the source state to the target state of the
        transition, note - a 'short-circuit' is when the source state is the same as the target state and the
        apply_short_circuit parameter is used to control if the leave() and enter() methods are invoked for such
        a circumstance, the guard is always invoked if it exists (either taken from the transition property or taken
        from the one_off_guard parameter) irrespective of whether an 'short-circuit' exists or not

        :param one_off_guard: temporary guard function that is used in place of the currently recorded guard function
        :param apply_short_circuit: if this transition is a 'short-circuit', then is this applied or not

        :return target state: to indicate that the transition fired successfully

        :exception GuardFailedException: raised if the guard prohibits the transaction as it is being processed
        """
        active_guard = one_off_guard if one_off_guard else self.guard

        if active_guard and not active_guard(self.source, self.target):
            # Cannot transition at this time as the active guard function has prohibited it, this will also raise a
            # fsm.exceptions.GuardFailedException exception to indicate this
            raise GuardFailedException(self.source, self.target, self)

        # Guard function must have passed so process this transition
        if self.source == self.target and apply_short_circuit:
            # This transition is a 'short-circuit', the apply_short_circuit parameter determines if the leave() and
            # enter() methods are invoked for such a circumstance (by default they are not)
            return self.target

        self.source.leave(self.target)
        self.target.enter(self.source)

        return self.target
