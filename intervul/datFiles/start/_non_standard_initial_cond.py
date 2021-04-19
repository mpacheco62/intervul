#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Start
from .non_standard_initial_cond import Components


class Non_standard_initial_cond(_Start):
    def __init__(self, read_by_file=False):
        self.mode = None

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        words = self.reader.words
        self.words = self.reader.words
        if words[0][:5] == 'COMPO':
            word = words.popleft()
            self._should_be(word, 'COMPONENTS')
            self.mode = Components(read_by_file=True)

    def __str__(self):
        text = "NON_STANDARD_INITIAL_COND"
        if self.mode is not None:
            text += ", " + str(self.mode)
        return text
