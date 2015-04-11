import os
import sys

topLevelPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src/automaton'
sys.path = [ topLevelPath ] + sys.path
#print( topLevelPath )
