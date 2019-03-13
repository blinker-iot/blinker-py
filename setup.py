#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='Blinker',
    version='0.2.0',
    author='i3water',
    description='Blinker library in python',
    long_description=open('README.md').read(),
    license='MIT',
    url='https://github.com/blinker-iot/blinker-py',
    packages=['Blinker', 'BlinkerAdapters', 'BlinkerUtility'],
    # package_dir={'Blinker':'', 'BlinkerAdapters':'', 'BlinkerUtility':''},
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: IoT device',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: IoT :: Libraries :: Python Modules',
    ]
)