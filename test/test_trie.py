# -*- coding: utf-8 -*-
# @author <marty.patrick@gmail.com>

from __future__ import absolute_import, print_function

from unittest import TestCase

from automaton.trie import build_trie


class BuildTrieTestCase(TestCase):
    def test_emptyword(self):
        words = ['']
        t = build_trie(words)
        expected = {'initial': 0, 'finals': [], 'transitions': {0: {}}}
        assert expected == t.to_dict()
        assert not t.accept('')

    def test_a(self):
        words = ['a']
        t = build_trie(words)
        expected = {'initial': 0, 'finals': [1], 'outputs': {1: ['a']}, 'transitions': {0: {'a': 1}, 1: {}}}
        assert expected == t.to_dict()
        assert not t.accept('')
        assert t.accept('a')
        assert not t.accept('aa')

    def test_a_and_emptyword(self):
        words = ['a', '']
        t = build_trie(words)
        expected = {'initial': 0, 'finals': [1], 'outputs': {1: ['a']}, 'transitions': {0: {'a': 1}, 1: {}}}
        assert expected == t.to_dict()

    def test_a_b(self):
        words = ['a', 'b']
        t = build_trie(words)
        expected = {'initial': 0, 'finals': [1, 2], 'outputs': {1: ['a'], 2: ['b']}, 'transitions': {0: {'a': 1, 'b': 2}, 1: {}, 2: {}}}
        assert expected == t.to_dict()
        assert not t.accept('')
        assert t.accept('a')
        assert t.accept('b')
        assert not t.accept('aa')
        assert not t.accept('ab')

    def test_aa_ab(self):
        words = ['aa', 'ab']
        t = build_trie(words)
        expected = {'initial': 0, 'finals': [2, 3], 'outputs': {2: ['aa'], 3: ['ab']}, 'transitions': {0: {'a': 1}, 1: {'a': 2, 'b': 3}, 2: {}, 3: {}}}
        assert expected == t.to_dict()
        assert not t.accept('')
        assert not t.accept('a')
        assert not t.accept('b')
        assert t.accept('aa')
        assert t.accept('ab')

    def test_a_aa_ab(self):
        words = ['a', 'aa', 'ab']
        t = build_trie(words)
        expected = {'initial': 0, 'finals': [1, 2, 3], 'outputs': {1: ['a'], 2: ['aa'], 3: ['ab']}, 'transitions': {0: {'a': 1}, 1: {'a': 2, 'b': 3}, 2: {}, 3: {}}}
        assert expected == t.to_dict()
        assert not t.accept('')
        assert t.accept('a')
        assert not t.accept('b')
        assert t.accept('aa')
        assert t.accept('ab')
