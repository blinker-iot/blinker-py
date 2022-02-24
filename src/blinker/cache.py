# -*- coding: utf-8 -*-

"""
"""

__author__ = 'stao'

import json
import os.path

from typing import Dict


class CacheData(object):
    def __init__(self, device: str):
        self.cache_file = ".{0}.json".format(device)

    def load(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file) as f:
                return json.load(f)
        else:
            return None

    def update(self, data: Dict):
        with open(self.cache_file) as f:
            json.dump(data, f)
