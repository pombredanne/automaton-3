# -*- coding: utf-8 -*-
# @author <marty.patrick@gmail.com>

from __future__ import absolute_import, print_function

from unittest import TestCase

from automaton.transition_matrix import MutableTransitionMatrix
from automaton.transition_matrix import MutableTransitionMatrixWithDefaultSuccessor


class MutableTransitionMatrixTestCase(TestCase):
    def test_add_state__has_state__get_states(self):
        tm = MutableTransitionMatrix(0)
        assert 1 == tm.get_num_states()
        assert tm.has_state(0)
        assert not tm.has_state(1)
        # add state
        s1 = tm.add_state()
        # test
        assert 2 == tm.get_num_states()
        assert tm.has_state(0)
        assert tm.has_state(s1)
        assert tm.has_state(0)
        assert tm.has_state(1)
        # check states
        self.assertEqual(tm.get_states(), [0, 1])

    def test_add_transition(self):
        # initial state
        s0 = 0
        # init transition matrix
        tm = MutableTransitionMatrix(s0)
        assert 1 == tm.get_num_states()
        assert 0 == tm.get_num_transitions()
        # states
        s1 = tm.add_state()
        assert 2 == tm.get_num_states()
        # add s0 a s1
        tm.add_transition(s0, 'a', s1)
        assert 2 == tm.get_num_states()
        assert 1 == tm.get_num_transitions()
        assert s1 == tm.get_target(s0, 'a')
        # add s0 b s0
        tm.add_transition(s0, 'b', s0)
        assert 2 == tm.get_num_states()
        assert 2 == tm.get_num_transitions()
        assert s1 == tm.get_target(s0, 'a')
        assert s0 == tm.get_target(s0, 'b')
        # add s1 a s1
        tm.add_transition(s1, 'a', s1)
        assert 2 == tm.get_num_states()
        assert 3 == tm.get_num_transitions()
        assert s1 == tm.get_target(s0, 'a')
        assert s0 == tm.get_target(s0, 'b')
        assert s1 == tm.get_target(s1, 'a')
        # add s1 b s1
        tm.add_transition(s1, 'b', s1)
        assert 2 == tm.get_num_states()
        assert 4 == tm.get_num_transitions()
        assert s1 == tm.get_target(s0, 'a')
        assert s0 == tm.get_target(s0, 'b')
        assert s1 == tm.get_target(s1, 'a')
        assert s1 == tm.get_target(s1, 'b')

    def test_get_target_none(self):
        s0 = 0
        tm = MutableTransitionMatrix(s0)
        assert None == tm.get_target(s0, 'a')


class MutableTransitionMatrixWithDefaultSuccessorTestCase(TestCase):
    def test_get_target(self):
        s0 = 0
        tm = MutableTransitionMatrixWithDefaultSuccessor(s0)
        assert None == tm.get_target(s0, 'a')
        assert s0 == tm.get_target_by_default(s0, 'a')
        s1 = tm.add_state()
        tm.add_transition(s0, 'a', s1)
        assert s1 == tm.get_target(s0, 'a')
        assert s1 == tm.get_target_by_default(s0, 'a')
        assert None == tm.get_target(s0, 'b')
        assert s0 == tm.get_target_by_default(s0, 'b')
