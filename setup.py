#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import, print_function

from setuptools import find_packages
from setuptools import setup

setup(
    name='automaton',
    version='0.0.1',
    license='CC0-1.0',
    description='FSM automaton and Aho Corasick implementation',
    packages=find_packages('src'),
    package_dir={'': 'src'},
)
