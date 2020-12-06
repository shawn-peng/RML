#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:42:00 2019

@author: yisupeng
"""


def write_fact(output, fact_format, obj_tuple):
    s = (fact_format % obj_tuple) + '\n'
    s = s.replace('-', '_').replace(':', '').lower()
    output.write(s)
