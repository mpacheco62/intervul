#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import _Control_data

class _Hourglass(_Control_data):
    pass

class Elastic(_Hourglass):
    def __str__(self):
        return "ELASTIC"
