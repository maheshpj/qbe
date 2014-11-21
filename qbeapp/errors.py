# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 18:55:46 2014

@author: p7107498
"""


class QBEError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)