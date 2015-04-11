# -*- coding: utf-8 -*-
# @author <marty.patrick@gmail.com>


from .fst import MutableFSTD
from .trie import build_trie


def get_letters( words ):
    return set( letter for word in words for letter in word )

def build_dma_complete( words , letters=None ):
    dma = build_trie( words )
    initial = dma.get_initial_state()
    queue = []
    if letters is None:
        letters = get_letters( words )
    for letter in letters:
        target = dma.get_target( initial , letter )
        if target is None:
            dma.add_transition( initial , letter , initial )
        else:
            queue.append( ( target , initial ) )
    while len( queue ) != 0:
        p , r = queue.pop( 0 )
        if dma.is_final_state( r ):
            dma.set_final_state( p )
            dma.add_outputs( p , dma.get_outputs( r ) )
        for letter in letters:
            q = dma.get_target( p , letter )
            s = dma.get_target( r , letter )
            if q is None:
                dma.add_transition( p , letter , s )
            else:
                queue.append( ( q , s ) )
    return dma


def build_dma_default( words , letters=None ):
    dma = build_trie( words , fst_factory=MutableFSTD )
    initial = dma.get_initial_state()
    queue = []
    if letters is None:
        letters = get_letters( words )
    for letter in letters:
        target = dma.get_target( initial , letter )
        if target is not None:
            queue.append( ( target , initial ) )
    while len( queue ) != 0:
        p , r = queue.pop( 0 )
        if dma.is_final_state( r ):
            dma.set_final_state( p )
            dma.add_outputs( p , dma.get_outputs( r ) )
        for letter in letters:
            q = dma.get_target( p , letter )
            s = dma.get_target_by_default( r , letter )
            if q is None:
                if s != initial:
                    dma.add_transition( p , letter , s )
            else:
                queue.append( ( q , s ) )
    return dma
