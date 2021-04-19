#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from .common import _baseElements
from .startingBlock import NewStart, Restart, OtherParam


class Starting(_baseElements):
    # Basado en check0.f
    def __init__(self, words=None, values=None):
        self.mode = NewStart(None)
        self.otherParam = OtherParam(reader, self.mode)

        if words is not None and values is not None:
            self._initByReader(reader, words, values)

    def _initByReader(self, reader, words, values, **kwargs):
        self.reader = reader
        word = words.popleft()
        if word[:5] == 'START':
            self._shouldBe(word, "START")
            self.mode = NewStart(reader, words, values)

        elif word[:5] == 'RESTA':
            self._shouldBe(word, "RESTART")
            self.mode = Restart(reader, words, values)

        else:
            self._expected(['START, RESTART'])

        self.otherParam = OtherParam(reader, mode=self.mode.mode,
                                     words=words, values=values)

    def __str__(self):
        text = str(self.mode) + str(self.otherParam)
        return text
