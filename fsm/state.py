"""
Author:     Chris Knowles
Date:       Oct 2020
Copyright:  University of Sunderland, (c) 2020
File:       state.py
Version:    1.0.0
Notes:      Digital version of the 'Deep Space D6' PnP board game from Tau Leader Games
            URL - https://www.tauleadergames.com/deep-space-d6/
                - State class to be extended by concrete application states as part of the operation of the FSM
"""

# Imports
from data_model.identified_entity import IdentifiedEntity
from fsm.transition import Transition
from fsm.exceptions import DuplicateTransitionError, NoTransitionsError, TransitionNotFoundError


# Consts
# Globals
# Functions


# Classes
class State(IdentifiedEntity):
    def __init__(self, name):
        """
        Initialiser for the State class

        :attr _name: name associated with this state, read only property

        :attr _transitions: set of all transitions from this (source state) state to other states (target states), this
                            is a private property and should not be accessed directly to ensure integrity

        :param name: name of this state as a string
        """
        super().__init__()
        self._name = name
        self._transitions = []

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        """
        Equality predicate method to check this state against another supplied state

        :param other: fsm.state.State object to check equality with

        :return boolean: return True if state objects evaluate to equal, otherwise return False
        """
        return self.uid == other.uid

    def __str__(self):
        """
        String representation of a fsm.state.State object

        :return string: string representation
        """
        return "state [{0}]:[{1}]".format(self.uid, self.name)

    def add_transition(self, target_state, guard=None):
        """
        Add a new fsm.transition.Transition object that has the provided target state object as its target state, this
        transition is then added to the set of transitions for this state, NOTE: since a set is being added    to, any
        duplicate transitions are disregarded and not added to the set

        :param target_state: fsm.state.State object to provide the target state of the transition being added
        :param guard: function object that acts as a guard for this transition

        :return nothing:

        :exception DuplicateTransitionError: raised if transition to be added is already in set of transitions
        """
        transition = Transition(self, target_state, guard=guard)

        if transition in self._transitions:
            raise DuplicateTransitionError(self, target_state)

        self._transitions.append(transition)

    def get_transition(self, target_state):
        """
        Method to find transition within this state's set of transitions, if there exists no matching transition in the
        set then return None

        :param target_state: fsm.state.State object that will match for finding the required transition

        :return transition: fsm.transition.Transition object returned if it is in the state's transitions set or None if
                            it does not
        """
        for transition in self._transitions:
            if transition.source == self and transition.target == target_state:
                return transition

        return None

    def remove_transition(self, target_state):
        """
        Remove the fsm.transition.Transition object that has the provided target state from the set of transitions for
        this state, if no matching transition exists then raise a TransitionNotFoundError

        :param target_state: fsm.state.State object to provide the target state of the transition being removed

        :return nothing:

        :exception TransitionNotFoundError: raised if no matching transition is found
        """
        transition = self.get_transition(target_state)

        if transition :
            self._transitions.remove(transition)
        else:
            raise TransitionNotFoundError(self, target_state)

    def clear_transitions(self):
        """
        Remove all fsm.transition.Transition objects from the transitions set for this state object

        :return nothing:
        """
        self._transitions.clear()

    def fire_transition(self, target_state=None, guard=None):
        """
        Method to fire the transition which has the supplied target state as its target, if None is supplied as the
        target transition then fire the first transition in the transitions list (this can be useful when there is only
        one transition from this state), raises the exception fsm.exceptions.NoTransitionsError if the transitions list
        is empty or raises the exception fsm.exceptions.TransitionNotFoundError if there is no matching transition in
        the state's list of transitions

        :param target_state: fsm.state.State object that will determine the match for the required transition
        :param guard: guard function to use during the firing of this transition (overriding any existing guard held by
                      the transition, referred to as a 'one-off guard')

        :return target state: target_state is returned once the transition has fired

        :exception NoTransitionsError: raised if transitions list is empty
        :exception TransitionNotFoundError: raised if no matching transition is found
        :exception GuardFailedException: is thrown if transition.fire() raises this exception due to the guard failing
        """
        if not self._transitions:
            raise NoTransitionsError(self)

        if target_state:
            transition = self.get_transition(target_state)

            if transition:
                return transition.fire(one_off_guard=guard)
            else:
                raise TransitionNotFoundError(self, target_state)
        else:
            return self._transitions[0].fire(one_off_guard=guard)

    def enter(self, state):
        """
        Abstract enter method expected to be overridden by derived classes

        :param state: fsm.state.State object that was left before entering this state

        :return nothing:
        """
        pass

    def leave(self, state):
        """
        Abstract leave method expected to be overridden by derived classes

        :param state: fsm.state.State object that will be entered after leaving this state

        :return nothing:
        """
        pass
