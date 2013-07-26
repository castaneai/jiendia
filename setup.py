#!/bin/env python
# -*- coding: utf8 -*-
from distutils.core import setup

setup(
    name = 'jiendia',
    version = '0.1',
    description = 'data parser for LaTale Online.',
    url = 'https://github.com/castaneai/jiendia',
    author = 'castaneai',
    packages = ['jiendia', 'jiendia.io', 'jiendia.io.archive'],
    package_dir = {'jiendia': 'src/jiendia'},
)
