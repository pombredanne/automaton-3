# -*- coding: utf-8 -*-
# @author <marty.patrick@gmail.com>

from __future__ import absolute_import, print_function

import copy


class MutableTransitionMatrix(object):

    def __init__(self, initial_state):
        self.trans_matrix = {}
        self.trans_matrix[initial_state] = {}
        self.last_state = initial_state

    def add_state(self):
        self.last_state += 1
        new_state = self.last_state
        self.trans_matrix[new_state] = {}
        return new_state

    def add_transition(self, source, letter, target):
        self.trans_matrix[source][letter] = target
        return self

    def get_target(self, source, letter):
        successors = self.trans_matrix.get(source, None)
        if successors is None:
            raise RuntimeError('Unknown source state: %(source)s' % locals())
        return successors.get(letter, None)

    def get_transitions(self, source):
        return self.trans_matrix[source]

    def get_num_transitions(self):
        return sum(len(transitions) for transitions in self.trans_matrix.values())

    def has_state(self, state):
        return state in self.trans_matrix

    def get_num_states(self):
        return len(self.trans_matrix.keys())

    def get_states(self):
        return sorted(self.trans_matrix.keys())

    def alphabet(self):
        # FIXME: This is obscure
        return sorted(set(letter for successors in self.trans_matrix.values() for letter in successors.keys()))

    def to_dict(self):
        return copy.deepcopy(self.trans_matrix)


class MutableTransitionMatrixWithDefaultSuccessor(MutableTransitionMatrix):

    def __init__(self, initial_state):
        MutableTransitionMatrix.__init__(self, initial_state)
        self.default_successor = initial_state

    def get_target_by_default(self, source, letter):
        target = self.get_target(source, letter)
        return self.default_successor if target is None else target

    def to_dict(self):
        tm = copy.deepcopy(self.trans_matrix)
        letters = self.alphabet()
        states = self.get_states()
        for state in states:
            for letter in letters:
                if self.get_target(state, letter) is None:
                    tm[state][letter] = self.default_successor
        return tm
