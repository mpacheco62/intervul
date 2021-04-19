#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Control_data


class _Smoothing(_Control_data):
    pass



class Discrete(_Smoothing):
    def __init__(self, read_by_file=False):
        self.values = [0, 0]

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        values = self.reader.values
        self.values = [values[0], values[1]]

    def __str__(self):
        text = "SMOOTHING: DISCRETE"
        if self.values[0] != 0:
            text += ": " + str(self.values[0])
            if self.values[1] != 0:
                text += ", " + str(self.values[1])
        return text


class Local(_Smoothing):
    def __str__(self):
        return "SMOOTHING: LOCAL"


def select():
    instance = _Smoothing()
    words = instance.reader.words

    if words[1][:5] == "DISCR":
        instance._should_be(words[1], "DISCRETE")
        return Discrete(read_by_file=True)

    elif words[1][:5] == "LOCAL":
        return Local()

    else:
        instance._expected(["DISCRETE", "LOCAL"])
