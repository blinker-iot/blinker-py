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
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        "SimpleWebSocketServer",
        "zeroconf",
        "paho-mqtt",
        "requests",
        "dbus-python",
        "pygobject",
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
    ]
)