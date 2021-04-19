#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Start


class _New_start(_Start):
    pass


class Initial(_New_start):
    def __str__(self):
        return "START, INITIAL"


class No_initial(_New_start):
    def __str__(self):
        return "START, NOINITIAL"


class Previous(_New_start):
    def __init__(self, read_by_file=False):
        self.timePrev = 0

        if read_by_file:
            self._initByReader()

    def _initByReader(self, **kwargs):
        values = self.reader.values
        if len(values) < 1:
            print("WARNING: in line " + str(self.reader.lineNum()) +
                  " after PREVIOUS is expected a value")
        self.timePrev = values.popleft()

    def __str__(self):
        return "START, PREVIOUS=" + str(self.timePrev)


def select():
    instance = _New_start()
    words = instance.reader.words
    word = words.popleft()

    if word[:5] == 'NOINI':
        instance._should_be(word, "NOINITIAL")
        return No_initial()

    elif word[:5] == 'INITI':
        instance._should_be(word, "INITIAL")
        return Initial()

    elif word[:5] == 'PREVI':
        instance._should_be(word, "PREVIOUS")
        return Previous(read_by_file=True)
    else:
        instance._expected(["NOINITIAL", "INITIAL", "PREVIOUS"],
                       additionalText="After START")

    return
