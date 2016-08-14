# -*- coding: utf-8 -*-
# @author <lambda.coder@gmail.com>

from collections import defaultdict

from .transition_matrix import MutableTransitionMatrix
from .transition_matrix import MutableTransitionMatrixWithDefaultSuccessor


class FSTException(Exception):
    pass


class FST:
    def __init__(self, initialState, transitionMatrix, finalStates, outputs):
        self.initialState_ = initialState
        self.transitionMatrix_ = transitionMatrix
        self.finals_ = finalStates
        self.output_ = outputs

    def get_num_states(self):
        return self.transitionMatrix_.get_num_states()

    def get_states(self):
        return self.transitionMatrix_.get_states()

    def get_initial_state(self):
        return self.initialState_

    def get_final_states(self):
        return sorted(self.finals_)

    def is_final_state(self, state):
        if not self.transitionMatrix_.has_state(state):
            raise FSTException('Unknown state : %s' % str(state))
        return state in self.finals_

    def get_letters(self):
        return self.transitionMatrix_.get_letters()

    def get_target(self, source, letter):
        return self.transitionMatrix_.get_target(source, letter)

    # set get_target method
    get_target_function = get_target

    def get_outputs(self, state):
        if not self.transitionMatrix_.has_state(state):
            raise FSTException('Unknown state : %s' % str(state))
        return self.output_.get(state, set())

    def get_stats(self):
        return {'numStates': self.get_num_states(), 'numFinalStates': len(self.get_final_states()),
                'numTransitions': self.transitionMatrix_.get_num_transitions() }

    def accept(self, word):
        state = self.get_initial_state()
        for letter in word:
            state = self.get_target_function(state, letter)
            if state is None:
                return False
        return self.is_final_state(state)

    def det_search(self, word):
        outputs = []
        state = self.get_initial_state()
        for i, letter in enumerate(word):
            state = self.get_target_function(state, letter)
            if state is None:
                break
            if self.is_final_state(state):
                for x in sorted(self.get_outputs(state)):
                    outputs.append((x, i - len(x) + 1, i + 1))
        return outputs

    def to_dict(self):
        d = {'transitions': self.transitionMatrix_.to_dict(), 'initial': self.initialState_,
             'finals': self.finals_}
        outputs = {}
        for state in self.get_states():
            outs = self.get_outputs(state)
            if len(outs) != 0:
                outputs[state] = sorted(outs)
        d['outputs'] = outputs
        return d

    def to_dot(self):
        dot = ["""digraph FST {
rankdir = LR;
label = "";
center = 1;
ranksep = "0.4";
nodesep = "0.25";"""]
        states = self.get_states()
        for state in states:
            dot.append('%d [label = "%d", shape = %s, style = bold, fontsize = 14]' % (
                state, state, 'doublecircle' if self.is_final_state(state) else 'circle'))
            successors = self.transitionMatrix_.get_transitions(state)
            letters = successors.keys()
            for letter in sorted(letters):
                target = successors[letter]
                dot.append('\t%d -> %d [label = "%s", fontsize = 14];' % (state, target, letter))
        dot.append('}')
        return '\n'.join(dot)

    def dump_(self, outputFileName, output):
        outputFile = open(outputFileName, 'wb')
        outputFile.write(output.encode('utf-8'))
        outputFile.close()
        return self

    def dump_dot(self, dotFileName):
        return self.dump_(dotFileName, self.to_dot())


class MutableFSTException(Exception):
    pass


class AbstractMutableFST(FST):
    def __init__(self, initialState, transitionMatrix):
        FST.__init__(self, initialState, transitionMatrix, set(), defaultdict(set))

    def set_final_state(self, state):
        if not self.transitionMatrix_.has_state(state):
            raise MutableFSTException('Unknown state : %s' % str(state))
        self.finals_.add(state)
        return self

    def add_output(self, state, output):
        if not self.transitionMatrix_.has_state(state):
            raise MutableFSTException('Unknown state : %s' % str(state))
        self.output_[state].add(output)
        return self

    def add_outputs(self, state, outputs):
        for output in outputs:
            self.add_output(state, output)
        return self

    def add_state(self):
        return self.transitionMatrix_.add_state()

    def add_transition(self, source, letter, target):
        if len(letter) == 0:
            raise MutableFSTException(
                'Epsilon transition not allowed : source state : %s , target state : %s ' % (source, target))
        if not self.transitionMatrix_.has_state(source):
            raise MutableFSTException('Unknown source state : %s' % str(source))
        if not self.transitionMatrix_.has_state(target):
            raise MutableFSTException('Unknown target state : %s' % str(target))
        self.transitionMatrix_.add_transition(source, letter, target)
        return self


class MutableFST(AbstractMutableFST):
    def __init__(self):
        AbstractMutableFST.__init__(self, 0, MutableTransitionMatrix(0))


class MutableFSTD(AbstractMutableFST):  # D for default successor
    def __init__(self):
        AbstractMutableFST.__init__(self, 0, MutableTransitionMatrixWithDefaultSuccessor(0))

    def get_target_by_default(self, source, letter):
        return self.transitionMatrix_.get_target_by_default(source, letter)

    # set get_target method
    get_target_function = get_target_by_default
