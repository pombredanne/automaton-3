# -*- coding: utf-8 -*-
# @author <marty.patrick@gmail.com>

from .fst import MutableFST


def build_trie( words , fst_factory=MutableFST ):
    automaton = fst_factory()
    for word in words:
        if len( word ) != 0:
            currentState = automaton.get_initial_state()
            for letter in word:
                targetState = automaton.get_target( currentState , letter )
                if targetState is None:
                    targetState = automaton.add_state()
                    automaton.add_transition( currentState , letter , targetState )
                currentState = targetState
            automaton.set_final_state( currentState )
            automaton.add_output( currentState , word )
    return automaton
