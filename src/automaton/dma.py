# -*- coding: utf-8 -*-
# @author <marty.patrick@gmail.com>

from __future__ import absolute_import, print_function

from automaton.fst import MutableFSTWithDefaultSucessor
from automaton.trie import build_trie


def alphabet(words):
    """
    Return a set of unique letters given a sequence of words
    """
    alphabet = set()
    for word in words:
        for letter in word:
            alphabet.add(letter)
    return alphabet


def build_dma_complete(words, alphabet=None):
    """
    DMA ? deterministic Mealy automata?
    """
    trie = build_trie(words)
    initial = trie.get_initial_state()
    queue = []
    if alphabet is None:
        alphabet = alphabet(words)

    for letter in alphabet:
        target = trie.get_target(initial, letter)
        if target is None:
            trie.add_transition(initial, letter, initial)
        else:
            queue.append((target, initial))

    while len(queue) != 0:
        p, r = queue.pop(0)
        if trie.is_final_state(r):
            trie.set_final_state(p)
            trie.add_outputs(p, trie.get_outputs(r))
        for letter in alphabet:
            q = trie.get_target(p, letter)
            s = trie.get_target(r, letter)
            if q is None:
                trie.add_transition(p, letter, s)
            else:
                queue.append((q, s))
    return trie


def build_dma_default(words, letters=None):
    dma = build_trie(words, fst_factory=MutableFSTWithDefaultSucessor)
    initial = dma.get_initial_state()
    queue = []
    if letters is None:
        letters = alphabet(words)
    for letter in letters:
        target = dma.get_target(initial, letter)
        if target is not None:
            queue.append((target, initial))
    while len(queue) != 0:
        p, r = queue.pop(0)
        if dma.is_final_state(r):
            dma.set_final_state(p)
            dma.add_outputs(p, dma.get_outputs(r))
        for letter in letters:
            q = dma.get_target(p, letter)
            s = dma.get_target_by_default(r, letter)
            if q is None:
                if s != initial:
                    dma.add_transition(p, letter, s)
            else:
                queue.append((q, s))
    return dma
