#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 Marcus Müller.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

class prioritizer(gr.basic_block):
    """
    docstring for block prioritizer
    """
    def __init__(self, consume_both = True):
        gr.basic_block.__init__(self,
            name="prioritizer",
            in_sig=[numpy.float32, numpy.float32],
            out_sig=[numpy.float32])
        self._consume_both = consume_both

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        ninput_items_required[0] = noutput_items
        ninput_items_required[1] = 0
#        print "asked to produce", noutput_items, "will need", ninput_items_required[0], ninput_items_required[1]

    def general_work(self, input_items, output_items):
        l_in = (len(input_items[0]), len(input_items[1]))
        l_out = len(output_items)
#        print "got", l_in, "space", l_out
        if l_in[1]: # length of input_items[1] != 0
            howmany = min(min(l_in[1], l_out),l_in[0]) # we might never write more output than there is space available!
            output_items[0][0:howmany] = input_items[1][0:howmany] #copy input1
            self.consume(1, howmany) #tell GNU Radio we've used howmany items from input1
            if self._consume_both:
                self.consume(0,howmany) #... from input0
#            print "consumed", howmany
            return howmany # we produced howmany items
        else: # we wouldn't be called if there was no input, so here l_in[0] != 0
            howmany = min(l_in[0], l_out)
            output_items[0][0:howmany] = input_items[0][0:howmany] #copy input0
            self.consume(0,howmany)
#            print "consumed 0 only", howmany
            return howmany
