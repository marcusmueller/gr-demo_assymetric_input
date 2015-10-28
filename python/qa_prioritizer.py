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

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from prioritizer import prioritizer

class qa_prioritizer (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block()
        self.dut = prioritizer(False)
        self.src0 = blocks.vector_source_f([0.0], repeat = True)
        self.src1 = blocks.vector_source_f([1.0], repeat = True)
        self.throttle0 = blocks.throttle(gr.sizeof_float, 1e6)
        self.throttle1 = blocks.throttle(gr.sizeof_float, 1e4) ## 1/100 of the 0 rate
        self.head = blocks.head(gr.sizeof_float, int(1e4)) # about one second
        self.sink = blocks.vector_sink_f()
        self.tb.connect(self.src0, self.throttle0)
        self.tb.connect(self.src1, self.throttle1)
        self.tb.connect(self.throttle0, (self.dut,0))
        self.tb.connect(self.throttle1, (self.dut,1))
        self.tb.connect(self.dut, self. head, self.sink)
    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        # set up fg
        self.tb.run()
        # check data
        data = self.sink.data()
        print "length", len(data)
        avg = sum(data)/len(data)
        print avg 
        self.assertAlmostEqual(avg, 1e-2, 3)


if __name__ == '__main__':
    gr_unittest.run(qa_prioritizer, "qa_prioritizer.xml")
