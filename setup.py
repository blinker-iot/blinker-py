#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "stao"

import setuptools

setuptools.setup(
    name="blinker-py",
    version="0.3.0",
    author="stao",
    author_email="werewolf_st@hotmail.com",
    description="Blinker library in python",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/blinker-iot/blinker-py",
    project_urls={
        "Bug Tracker": "https://github.com/blinker-iot/blinker-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'aiohttp~=3.7.4',
        'certifi~=2021.10.8',
        'loguru~=0.5.3',
        'paho-mqtt~=1.6.1',
        'Rx~=3.2.0',
        "websockets~=10.2",
        'apscheduler~=3.9.1',
        'getmac~=0.8.3',
        'zeroconf~=0.38.4',
        'requests~=2.27.1',
    ],
)
