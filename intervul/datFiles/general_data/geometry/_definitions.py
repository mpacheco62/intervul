#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .._definitions import _General_data


class _Geometry(_General_data):
    pass



class Interpolate(_Geometry):
    def __str__(self):
        return "INTERPOLATE"

class Noninterpolate(_Geometry):
    def __str__(self):
        return "NONINTERPOLATE"

