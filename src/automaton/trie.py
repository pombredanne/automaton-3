# -*- coding: utf-8 -*-
# @author <marty.patrick@gmail.com>

from __future__ import absolute_import, print_function

from automaton.fst import MutableFST


def build_trie(keys, fst_factory=MutableFST):
    automaton = fst_factory()
    for key in keys:
        if len(key) != 0:
            current_state = automaton.get_initial_state()
            for letter in key:
                target_state = automaton.get_target(current_state, letter)
                if target_state is None:
                    target_state = automaton.add_state()
                    automaton.add_transition(current_state, letter, target_state)
                current_state = target_state
            automaton.set_final_state(current_state)
            automaton.add_output(current_state, key)
    return automaton
