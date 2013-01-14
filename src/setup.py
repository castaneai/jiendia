#!python
# -*- coding: utf8 -*-
from distutils.core import setup

setup(
    name = 'jiendia',
    version = '0.1',
    description = 'data parser for LaTale Online.',
    url = '',
    author = 'castaneai',
    packages = ['jiendia', 'jiendia.io', 'jiendia.sql', 'jiendia.sql.normalization'],
    package_dir = {'jiendia': 'src/jiendia'},
)