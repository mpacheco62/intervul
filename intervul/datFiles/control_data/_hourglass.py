#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Control_data
from .hourglass import Elastic

class Hourglass(_Control_data):
    def __init__(self, read_by_file=False):
        self.param = 0
        self.elastic = None

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        words = self.reader.words
        values = self.reader.values
        if words[1][:5] == "ELAST":
            self._should_be(words[1], "ELASTIC")
            self.elastic = Elastic()

        self.param = values[0]

    def __str__(self):
        text = "HOURGLASS"
        if self.elastic is not None:
            text += ": " + str(self.elastic)

        if self.param != 0:
            text += ", " + str(self.param)

        return text
