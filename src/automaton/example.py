# -*- coding: utf-8 -*-
# @author <marty.patrick@gmail.com>

from .dma import build_dma_complete
from .dma import build_dma_default

words = [ 'aa' , 'abaaa' , 'abab' ]

dma = build_dma_complete( words )
dma.dump_dot( 'dma.dot' )

dmad = build_dma_default( words )
dmad.dump_dot( 'dmad.dot' )
