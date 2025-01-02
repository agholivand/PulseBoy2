# -*- coding: utf-8 -*-
"""
Created on Mon Nov 02 18:16:20 2015

@author: Andrew
"""

import numpy
import math


def binary_to_digital_map(bin_buffer):
    # If we have a sequence of 1s and 0s corresponding to digital ON and OFF times,
    # we want to map this to digital commands that
    # the digital ports can read and implement.
    # Input should be mapped as a 2d numpy array (dtype=numpy.uint32), rows are individual lines, columns
    # are continuous time points. Ignores sampling rate until we tell NIDAQmx what it is.   
    
    digital = numpy.zeros((bin_buffer.shape[0], bin_buffer.shape[1]))
        
    n_lines = digital.shape[0]
    
    for line in range(n_lines):
        digital[line] = bin_buffer[line] * math.pow(2, line)
    
    return numpy.uint32(digital)
