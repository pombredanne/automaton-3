# -*- coding: utf-8 -*-
# @author <marty.patrick@gmail.com>

from __future__ import absolute_import, print_function

from unittest import TestCase

from automaton.fst import MutableFSTException
from automaton.fst import MutableFST
from automaton.fst import MutableFSTD


class MutableFSTTestCase(TestCase):
    def test_construction(self):
        f = MutableFST()
        assert [] == f.get_letters()
        s0 = f.get_initial_state()
        assert 0 == s0
        assert [s0] == f.get_states()
        assert [] == f.get_final_states()
        expected = {'initial': s0, 'finals': [], 'transitions': {s0: {}}}
        assert expected == f.to_dict()

    def test_add_state(self):
        f = MutableFST()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        assert [s0, s1] == f.get_states()
        expected = {'initial': s0, 'finals': [], 'transitions': {s0: {}, s1: {}}}
        assert expected == f.to_dict()

        s2 = f.add_state()
        assert [s0, s1, s2] == f.get_states()
        expected = {'initial': s0, 'finals': [], 'transitions': {s0: {}, s2: {}, s1: {}}}
        assert expected == f.to_dict()

    def test_add_transition_with_empty_word(self):
        f = MutableFST()
        s0 = f.get_initial_state()
        self.assertRaises(MutableFSTException, f.add_transition, s0, '', s0)

    def test_add_transition(self):
        f = MutableFST()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        s2 = f.add_state()
        # s0 a s1
        f.add_transition(s0, 'a', s1)
        expected = {'initial': s0, 'finals': [], 'transitions': {s0: {'a': s1}, s1: {}, s2: {}}}
        assert expected == f.to_dict()
        t = f.get_target(s0, 'a')
        assert s1 == t
        assert ['a'] == f.get_letters()
        # s0 b s2
        f.add_transition(s0, 'b', s2)
        expected = {'initial': s0, 'finals': [], 'transitions': {s0: {'a': s1, 'b': s2}, s1: {}, s2: {}}}
        assert expected == f.to_dict()
        t = f.get_target(s0, 'b')
        assert s2 == t
        assert ['a', 'b'] == f.get_letters()
        # s1 a s0
        f.add_transition(s1, 'a', s0)
        expected = {'initial': s0, 'finals': [], 'transitions': {s0: {'a': s1, 'b': s2}, s1: {'a': s0}, s2: {}}}
        assert expected == f.to_dict()
        t = f.get_target(s1, 'a')
        assert s0 == t
        # s0 a s2
        f.add_transition(s0, 'a', s2)
        expected = {'initial': s0, 'finals': [], 'transitions': {s0: {'a': s2, 'b': s2}, s1: {'a': s0}, s2: {}}}
        assert expected == f.to_dict()
        t = f.get_target(s0, 'a')
        assert s2 == t

    def test_final_state(self):
        f = MutableFST()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        assert [] == f.get_final_states()
        f.set_final_state(s1)
        assert [s1] == f.get_final_states()
        expected = {'initial': s0, 'finals': [s1], 'transitions': {s0: {}, s1: {}}}
        assert expected == f.to_dict()
        s2 = f.add_state()
        f.set_final_state(s2)
        assert [s1, s2] == f.get_final_states()
        expected = {'initial': s0, 'finals': [s1, s2], 'transitions': {s0: {}, s1: {}, s2: {}}}
        assert expected == f.to_dict()


    def test_is_final_state(self):
        f = MutableFST()
        s0 = f.get_initial_state()
        assert not f.is_final_state(s0)
        s1 = f.add_state()
        f.set_final_state(s1)
        assert not f.is_final_state(s0)
        assert f.is_final_state(s1)
        f.set_final_state(s0)
        assert f.is_final_state(s0)

    def test_accept(self):
        # build some fsa
        f = MutableFST()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        f.add_transition(s0, 'a', s1).add_transition(s1, 'a', s0).set_final_state(s1)
        expected = {'initial': s0, 'finals': [s1], 'transitions': {s0: {'a': s1}, s1: {'a': s0}}}
        assert expected == f.to_dict()
        # test accept
        # # empty word is not accepted
        assert not f.accept('')
        # # a is accepted
        assert f.accept('a')
        # # aa is not accepted
        assert not f.accept('aa')
        # # aaa is not accepted
        assert f.accept('aaa')
        # # b is not accepted
        assert not f.accept('b')

    def test_det_search_ab_babb_bb(self):
        # build some fsa
        f = MutableFST()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        s2 = f.add_state()
        s3 = f.add_state()
        s4 = f.add_state()
        s5 = f.add_state()
        s6 = f.add_state()
        s7 = f.add_state()
        f.add_transition(s0, 'a', s1).add_transition(s0, 'b', s3)
        f.add_transition(s1, 'a', s1).add_transition(s1, 'b', s2)
        f.add_transition(s2, 'a', s4).add_transition(s2, 'b', s7)
        f.add_transition(s3, 'a', s4).add_transition(s3, 'b', s7)
        f.add_transition(s4, 'a', s1).add_transition(s4, 'b', s5)
        f.add_transition(s5, 'a', s4).add_transition(s5, 'b', s6)
        f.add_transition(s6, 'a', s4).add_transition(s6, 'b', s7)
        f.add_transition(s7, 'a', s4).add_transition(s7, 'b', s7)
        f.set_final_state(s2).set_final_state(s5).set_final_state(s6).set_final_state(s7)
        f.add_output(s2, 'ab').add_output(s5, 'ab').add_output(s6, 'bb').add_output(s6, 'babb').add_output(s7, 'bb')
        expected = {'initial': s0, 'finals': [s2, s5, s6, s7], 'outputs': {s2: ['ab'], s5: ['ab'], s6: ['babb', 'bb'], s7: ['bb']}, 'transitions': {s0: {'a': s1, 'b': s3}, s1: {'a': s1, 'b': s2}, s2: {'a': s4, 'b': s7}, s3: {'a': s4, 'b': s7}, s4: {'a': s1, 'b': s5}, s5: {'a': s4, 'b': s6}, s6: {'a': s4, 'b': s7}, s7: {'a': s4, 'b': s7}}}
        assert expected == f.to_dict()
        self.assertEqual(f.get_letters(), ['a', 'b'])
        # test det_search simulation on babba
        assert s3 == f.get_target(s0, 'b')
        assert s4 == f.get_target(s3, 'a')
        assert s5 == f.get_target(s4, 'b')
        assert s6 == f.get_target(s5, 'b')
        assert s4 == f.get_target(s6, 'a')
        # test det_search
        outputs = f.det_search('babba')
        # babba
        # 01234
        self.assertEqual(outputs, [('ab', 1, 3), ('babb', 0, 4), ('bb', 2, 4)])
        for o in outputs:
            self.assertEqual('babba'[o[1]:  o [2]], o[0])

    def test_det_search_ab_aa(self):
        f = MutableFST()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        s2 = f.add_state()
        s3 = f.add_state()
        f.add_transition(s0, 'a', s1)
        f.add_transition(s1, 'a', s2).add_transition(s1, 'b', s3)
        f.set_final_state(s2).set_final_state(s3)
        f.add_output(s2, 'aa').add_output(s3, 'ab')
        assert [] == f.det_search('a ab aa')

    def test_output_stuff(self):
        f = MutableFST()
        s0 = f.get_initial_state()
        assert set() == f.get_outputs(s0)
        self.assertEqual(f.to_dict(), {'initial':  s0, 'finals':  [], 'transitions':  {s0:  {}}})
        f.add_output(s0, 1)
        self.assertEqual(f.get_outputs(s0), {1 })
        self.assertEqual(f.to_dict(), {'initial':  s0, 'finals':  [], 'outputs':  {s0:  [1]}, 'transitions':  {s0:  {}}})
        f.add_output(s0, 2)
        self.assertEqual(f.get_outputs(s0), {1, 2 })
        self.assertEqual(f.to_dict(), {'initial':  s0, 'finals':  [], 'outputs':  {s0:  [1, 2]}, 'transitions':  {s0:  {}}})
        f.add_output(s0, 1)
        self.assertEqual(f.get_outputs(s0), {1, 2 })
        self.assertEqual(f.to_dict(), {'initial':  s0, 'finals':  [], 'outputs':  {s0:  [1, 2]}, 'transitions':  {s0:  {}}})

    def test_get_stats(self):
        # build some fsa
        f = MutableFST()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        s2 = f.add_state()
        s3 = f.add_state()
        s4 = f.add_state()
        s5 = f.add_state()
        s6 = f.add_state()
        s7 = f.add_state()
        f.add_transition(s0, 'a', s1).add_transition(s0, 'b', s3)
        f.add_transition(s1, 'a', s1).add_transition(s1, 'b', s2)
        f.add_transition(s2, 'a', s4).add_transition(s2, 'b', s7)
        f.add_transition(s3, 'a', s4).add_transition(s3, 'b', s7)
        f.add_transition(s4, 'a', s1).add_transition(s4, 'b', s5)
        f.add_transition(s5, 'a', s4).add_transition(s5, 'b', s6)
        f.add_transition(s6, 'a', s4).add_transition(s6, 'b', s7)
        f.add_transition(s7, 'a', s4).add_transition(s7, 'b', s7)
        f.set_final_state(s2).set_final_state(s5).set_final_state(s6).set_final_state(s7)
        f.add_output(s2, 'ab').add_output(s5, 'ab').add_output(s6, 'bb').add_output(s6, 'babb').add_output(s7, 'bb')
        expected = {'initial': s0, 'finals': [s2, s5, s6, s7], 'outputs': {s2: ['ab'], s5: ['ab'], s6: ['babb', 'bb'], s7: ['bb']}, 'transitions': {s0: {'a': s1, 'b': s3}, s1: {'a': s1, 'b': s2}, s2: {'a': s4, 'b': s7}, s3: {'a': s4, 'b': s7}, s4: {'a': s1, 'b': s5}, s5: {'a': s4, 'b': s6}, s6: {'a': s4, 'b': s7}, s7: {'a': s4, 'b': s7}}}
        assert expected == f.to_dict()
        # test get_stats
        expected = {'num_states': 8, 'num_final_states': 4, 'num_transitions': 16}
        assert expected == f.get_stats()

    def test_to_dot(self):
        f = MutableFST()
        # initial state
        s0 = f.get_initial_state()
        expected_dot = """digraph FST {
rankdir = LR;
label = "";
center = 1;
ranksep = "0.4";
nodesep = "0.25";
0 [label = "0",shape = circle,style = bold,fontsize = 14]
}"""
        assert expected_dot.split('\n') == f.to_dot().split('\n')
        # add state
        s1 = f.add_state()
        expected_dot = """digraph FST {
rankdir = LR;
label = "";
center = 1;
ranksep = "0.4";
nodesep = "0.25";
0 [label = "0",shape = circle,style = bold,fontsize = 14]
1 [label = "1",shape = circle,style = bold,fontsize = 14]
}"""
        assert expected_dot.split('\n') == f.to_dot().split('\n')
        # add transition
        f.add_transition(s0, 'a', s1)
        expected_dot = """digraph FST {
rankdir = LR;
label = "";
center = 1;
ranksep = "0.4";
nodesep = "0.25";
0 [label = "0",shape = circle,style = bold,fontsize = 14]
	0 -> 1 [label = "a",fontsize = 14];
1 [label = "1",shape = circle,style = bold,fontsize = 14]
}"""
        assert expected_dot.split('\n') == f.to_dot().split('\n')
        # add final state
        f.set_final_state(s1)
        # check to_dot
        expected_dot = """digraph FST {
rankdir = LR;
label = "";
center = 1;
ranksep = "0.4";
nodesep = "0.25";
0 [label = "0",shape = circle,style = bold,fontsize = 14]
	0 -> 1 [label = "a",fontsize = 14];
1 [label = "1",shape = doublecircle,style = bold,fontsize = 14]
}"""
        assert expected_dot.split('\n') == f.to_dot().split('\n')


class MutableFSTDTestCase(TestCase):

    def test_matching(self):
        f = MutableFSTD()
        s0 = f.get_initial_state()
        s1 = f.add_state()
        s2 = f.add_state()
        s3 = f.add_state()
        f.add_transition(s0, 'a', s1)
        f.add_transition(s1, 'a', s2).add_transition(s1, 'b', s3)
        f.set_final_state(s2).set_final_state(s3)
        f.add_output(s2, 'aa').add_output(s3, 'ab')

        expected = [('ab', 2, 4), ('aa', 5, 7)]
        assert expected == f.det_search('a ab aa')
