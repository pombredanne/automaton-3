# -*- coding: utf-8 -*-
# @author <marty.patrick@gmail.com>

import copy




class MutableTransitionMatrix:
    def __init__( self , initialState ):
        self.tm_ = {}
        self.tm_[initialState] = {}
        self.lastState_ = initialState


    def add_state( self ):
        self.lastState_ += 1
        newState = self.lastState_
        self.tm_[newState] = {}
        return newState


    def add_transition( self , source , letter , target ):
        self.tm_[ source ][ letter ] = target
        return self


    def get_target( self , source , letter ):
        successors = self.tm_.get( source , None )
        if successors is None:
            raise RuntimeError( 'Unknown source state : %s' % str( source ) )
        return successors.get( letter , None )


    def get_transitions( self , source ):
        return self.tm_[source]


    def get_num_transitions( self ):
        return sum( len( transitions ) for transitions in self.tm_.values() )


    def has_state( self , state ):
        return state in self.tm_


    def get_num_states( self ):
        return len( self.tm_.keys() )


    def get_states( self ):
        return sorted( self.tm_.keys() )


    def get_letters( self ):
        return sorted( set( letter for successors in self.tm_.values() for letter in successors.keys() ) )


    def to_dict( self ):
        return copy.deepcopy( self.tm_ )




class MutableTransitionMatrixWithDefaultSuccessor( MutableTransitionMatrix ):
    def __init__( self , initialState ):
        MutableTransitionMatrix.__init__( self , initialState )
        self.defaultSuccessor_ = initialState


    def get_target_by_default( self , source , letter ):
        target = self.get_target( source , letter )
        return self.defaultSuccessor_ if target is None else target


    def to_dict( self ):
        tm = copy.deepcopy( self.tm_ )
        letters = self.get_letters()
        states = self.get_states()
        for state in states:
            for letter in letters:
                if self.get_target( state , letter ) is None:
                    tm[state][letter] = self.defaultSuccessor_
        return tm
