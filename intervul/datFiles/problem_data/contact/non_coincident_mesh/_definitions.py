#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .._definitions import _Contact


class _Non_coincident_mesh(_Contact):
    pass


class Non_linearized(_Non_coincident_mesh):
    def __init__(self, read_by_file=False):
        self.mode = 0  # options 0 y 1

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        values = self.reader.values
        if len(values) > 0:
            self.mode = values.popleft()
        else:
            self._expected_value("After Non Linearized must be a value")

    def __str__(self):
        return "NON_LINEARIZED_COMPUTATION_OF_N: " + str(self.mode)
