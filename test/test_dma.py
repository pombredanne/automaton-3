# -*- coding: utf-8 -*-
# @author <marty.patrick@gmail.com>

from __future__ import absolute_import, print_function

from unittest import TestCase

from automaton.dma import build_dma_default


class BuildDMATestCase(TestCase):
    def test_a_ab(self):
        words = ['a', 'ab']
        d = build_dma_default(words)
        # check automaton
        expected = {
            'initial':  0 ,
            'finals':  [1, 2],
            'outputs':  {1:  ['a'], 2:  ['ab']},
            'transitions':  {0:  {'a':  1 , 'b':  0 }, 1:  {'a':  1 , 'b':  2 }, 2:  {'a':  1 , 'b':  0 }}}
        assert expected == d.to_dict()


    def test_aa_ab(self):
        words = ['aa', 'ab']
        d = build_dma_default(words)
        # check automaton
        expected = {'initial':  0,
                    'finals':  [2, 3],
                    'outputs':  {2:  ['aa'], 3:  ['ab']},
                    'transitions':  {0:  {'a': 1, 'b': 0}, 1:  {'a':  2, 'b':  3}, 2:  {'a':  2, 'b':  3}, 3 : {'a':  1, 'b':  0}}}
        assert expected == d.to_dict()
        # check accepted words
        assert not d.accept('')
        assert not d.accept('a')
        assert not d.accept('b')
        assert d.accept('aa')
        assert d.accept('ab')
        assert d.accept('aaa')
        assert d.accept('aab')
        assert d.accept('abab')
        assert d.accept('abaaa')
        assert not d.accept('c')
        assert not d.accept('ac')


    def test_aa_abaaa_abab(self):
        words = ['aa', 'abaaa', 'abab']
        d = build_dma_default(words)
        # check automaton
        self.assertEqual(d.to_dict(), {'initial':  0 , 'finals':  [2, 5, 6, 7], 'outputs':  {2:  ['aa'], 5:  ['aa'], 6:  ['aa', 'abaaa'], 7:  ['abab']}, 'transitions':  {0:  {'a':  1 , 'b':  0 }, 1:  {'a':  2 , 'b':  3 }, 2:  {'a':  2 , 'b':  3 }, 3:  {'a':  4 , 'b':  0 }, 4:  {'a':  5 , 'b':  7 }, 5:  {'a':  6 , 'b':  3 }, 6:  {'a':  2 , 'b':  3 }, 7:  {'a':  4 , 'b':  0 }}})
        # check accepted words
        assert not d.accept('')
        assert not d.accept('a')
        assert not d.accept('b')
        assert d.accept('aa')
        assert not d.accept('ab')
        assert d.accept('abab')
        assert d.accept('abaaa')
        assert not d.accept('c')
        assert not d.accept('ac')


    def test_ab_babb_bb(self):
        words = ['ab', 'babb', 'bb']
        d = build_dma_default(words)
        # check automaton
        self.assertEqual(d.to_dict(), {'initial':  0 , 'finals':  [2, 5, 6, 7], 'outputs':  {2:  ['ab'], 5:  ['ab'], 6:  ['babb', 'bb'], 7:  ['bb']}, 'transitions':  {0:  {'a':  1 , 'b':  3 }, 1:  {'a':  1 , 'b':  2 }, 2:  {'a':  4 , 'b':  7 }, 3:  {'a':  4 , 'b':  7 }, 4:  {'a':  1 , 'b':  5 }, 5:  {'a':  4 , 'b':  6 }, 6:  {'a':  4 , 'b':  7 }, 7:  {'a':  4 , 'b':  7 }}})
        # test det_search on babba
        # babba
        # 012345
        self.assertEqual(d.det_search('babba'), [('ab', 1, 3), ('babb', 0, 4), ('bb', 2, 4)])
