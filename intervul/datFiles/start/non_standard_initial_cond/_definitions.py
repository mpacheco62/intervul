#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import _Start

class _Non_standard_initial_cond(_Start):
    pass


class Components(_Non_standard_initial_cond):
    def __init__(self, read_by_file=False):
        self.nstress = 0
        self.ninternal = 0

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        values = self.reader.values
        self.values = self.reader.values
        self.nstress = values.popleft()
        self.ninternal = values.popleft()

    def __str__(self):
        text = "COMPONENTS"
        if self.nstress != 0:
            text += ": " + str(self.nstress)
            if self.ninternal != 0:
                text += ", " + str(self.ninternal)
        return text
