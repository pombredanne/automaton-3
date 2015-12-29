# -*- coding: utf-8 -*-
# @author <marty.patrick@gmail.com>

from __future__ import absolute_import, print_function

from collections import defaultdict

from automaton.transition_matrix import MutableTransitionMatrix
from automaton.transition_matrix import MutableTransitionMatrixWithDefaultSuccessor


class FSTException(Exception):
    pass


class FST(object):
    """
    Possibly a https://en.wikipedia.org/wiki/Finite_state_transducer ?
    https://www.google.com/search?q=Finite+state+transducer+Mealy+automata
    """
    def __init__(self, initial_state, transition_matrix, final_states, outputs):
        self.initial_state = initial_state
        self.transition_matrix = transition_matrix
        self.finals = final_states
        self.output = outputs

    def get_num_states(self):
        return self.transition_matrix.get_num_states()

    def get_states(self):
        return self.transition_matrix.get_states()

    def get_initial_state(self):
        return self.initial_state

    def get_final_states(self):
        return sorted(self.finals)

    def is_final_state(self, state):
        if not self.transition_matrix.has_state(state):
            raise FSTException('Unknown state: %(state)s' % locals())
        return state in self.finals

    def alphabet(self):
        return self.transition_matrix.alphabet()

    def get_target(self, source, letter):
        return self.transition_matrix.get_target(source, letter)

    # set get_target method
    get_target_function = get_target

    def get_outputs(self, state):
        """
        Return a set of outputs for a state.
        """

        if not self.transition_matrix.has_state(state):
            raise FSTException('Unknown state: %(state)s' % locals())
        return self.output.get(state, set())

    def get_stats(self):
        """
        Return a dictionary of statistics on the automaton.
        """
        num_transitions = self.transition_matrix.get_num_transitions()
        return {
            'num_states': self.get_num_states(),
            'num_final_states': len(self.get_final_states()),
            'num_transitions': num_transitions
       }

    def accept(self, word):
        """
        Return True if word if found in automaton.
        """
        current_state = self.get_initial_state()
        for letter in word:
            current_state = self.get_target_function(current_state, letter)
            if current_state is None:
                return False
        return self.is_final_state(current_state)

    def _det_search(self, word):
        """
        Search for word and yield tuples of (letter, start pos, end pos)
        """
        current_state = self.get_initial_state()
        for letter_pos, letter in enumerate(word):
            current_state = self.get_target_function(current_state, letter)
            if current_state is None:
                break
            if self.is_final_state(current_state):
                for x in sorted(self.get_outputs(current_state)):
                    yield x, letter_pos - len(x) + 1, letter_pos + 1

    def det_search(self, word):
        """
        det == deterministic?
        Search for word and return a list of  tuples of (letter, start pos, end pos)
        """
        return list(self._det_search(word))

    def to_dict(self):
        """
        Return a dictionary representing self.
        """
        d = dict(
            transitions=self.transition_matrix.to_dict(),
            initial=self.initial_state,
            finals=sorted(self.finals)
        )
        outputs = {}
        for state in self.get_states():
            state_outputs = self.get_outputs(state)
            if len(state_outputs):
                outputs[state] = sorted(state_outputs)
        if len(outputs):
            d['outputs'] = outputs
        return d

    def to_dot(self):
        """
        Return a string representing self in Graphviz dot format.
        """
        dot = ["""digraph FST {
rankdir = LR;
label = "";
center = 1;
ranksep = "0.4";
nodesep = "0.25";"""]
        states = self.get_states()
        for state in states:
            shape = self.is_final_state(state) and 'doublecircle' or 'circle'
            dot.append('%(state)d [label = "%(state)d",shape = %(shape)s,style = bold,fontsize = 14]' % locals())
            successors = self.transition_matrix.get_transitions(state)
            letters = successors.keys()
            for letter in sorted(letters):
                target = successors[letter]
                dot.append('\t%d -> %d [label = "%s",fontsize = 14];' % (state, target, letter))
        dot.append('}')
        return '\n'.join(dot)

    def dump(self, location, output):
        """
        Dump output to location.
        """
        with open(location, 'wb') as output_file:
            output_file.write(output.encode('utf-8'))
        return self

    def dump_to_dot(self, location):
        """
        Dump self in a graphviz dot format to location.
        """
        return self.dump(location, self.to_dot())


class MutableFSTException(Exception):
    pass


class AbstractMutableFST(FST):
    def __init__(self, initial_state, transition_matrix):
        FST.__init__(self, initial_state, transition_matrix, set(), defaultdict(set))

    def set_final_state(self, state):
        if not self.transition_matrix.has_state(state):
            raise MutableFSTException('Unknown state: % s' % str(state))
        self.finals.add(state)
        return self

    def add_output(self, state, output):
        if not self.transition_matrix.has_state(state):
            raise MutableFSTException('Unknown state: % s' % str(state))
        self.output[state].add(output)
        return self

    def add_outputs(self, state, outputs):
        for output in outputs:
            self.add_output(state, output)
        return self

    def add_state(self):
        return self.transition_matrix.add_state()

    def add_transition(self, source, letter, target):
        if len(letter) == 0:
            raise MutableFSTException('Epsilon transition not allowed: source state: %(source)s,target state: %(target)s ' % locals())

        if not self.transition_matrix.has_state(source):
            raise MutableFSTException('Unknown source state: %(source)s' % locals())

        if not self.transition_matrix.has_state(target):
            raise MutableFSTException('Unknown target state: %(target)s' % locals())

        self.transition_matrix.add_transition(source, letter, target)
        return self


class MutableFST(AbstractMutableFST):
    def __init__(self):
        AbstractMutableFST.__init__(self, 0, MutableTransitionMatrix(0))


class MutableFSTWithDefaultSucessor(AbstractMutableFST):
    # D for default successor
    def __init__(self):
        AbstractMutableFST.__init__(self, 0, MutableTransitionMatrixWithDefaultSuccessor(0))

    def get_target_by_default(self, source, letter):
        return self.transition_matrix.get_target_by_default(source, letter)

    # set get_target method
    get_target_function = get_target_by_default
