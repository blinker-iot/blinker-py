# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

import os.path
import json


class JsonFile(object):
    @staticmethod
    async def save(path, data):
        with open(path) as f:
            json.dump(data, f)

    @staticmethod
    async def load(path):
        if os.path.exists(path):
            with open(path) as f:
                content = json.load(f)
            return content
        else:
            return {}
