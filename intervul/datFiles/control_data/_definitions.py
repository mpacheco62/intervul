#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .._common import Base_dat


class _Control_data(Base_dat):
    pass


class Postprocess(_Control_data):
    def __str__(self):
        return "POSTPROCESS"


class Renumbering(_Control_data):
    def __str__(self):
        return "RENUMBERING"


class Cpulimit(_Control_data):
    def __init__(self, read_by_file=False):
        self.time = 10

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        values = self.reader.values
        self.time = values[0]

    def __str__(self):
        text = ''
        if self.time != 0:
            text = "CPULIMIT: " + str(self.time)
        return text


class Datal(_Control_data):
    def __init__(self, read_by_file=False):
        self.nblim = 0

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        values = self.reader.values
        self.nblim = values[0]

    def __str__(self):
        text = ''
        if self.nblim != 0:
            text = "DATAL: " + str(self.nblim)

        return text






