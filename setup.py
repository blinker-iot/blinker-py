# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='Blinker',
    version='0.1.0',
    author='i3water',
    packages=['Blinker', 'BlinkerAdapters', 'BlinkerUtility'],
    # package_dir={'Blinker':'', 'BlinkerAdapters':'', 'BlinkerUtility':''},
    url='https://github.com/blinker-iot/blinker-py',
    description='Blinker library in python',
    long_description=open('README.md').read()
)