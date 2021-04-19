#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .._definitions import _Contact


class _Augmented_lagrange(_Contact):
    pass


class Version(_Augmented_lagrange):
    def __init__(self, read_by_file=False):
        self.number = 1  # Por poner algo

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        values = self.reader.values
        self.number = values.popleft()

    def __str__(self):
        return "VERSION: " + str(self.number)
