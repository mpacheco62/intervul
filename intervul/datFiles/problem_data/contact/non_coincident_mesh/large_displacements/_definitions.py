#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .._definitions import _Non_coincident_mesh


class _large_displacements(_Non_coincident_mesh):
    pass


class Non_linearized(_large_displacements):
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


class Maximum_gap(_large_displacements):
    def __init__(self, read_by_file=False):
        self.value = 1.0

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        values = self.reader.values
        if len(values) > 0:
            self.value = values.popleft()

        else:
            self._expected_value("After Maximum Gap must be a value")

    def __str__(self):
        return "MAXIMUM_GAP_FOR_POSSIBLE_CONTACT= " + str(self.value)


class Skipping(_large_displacements):
    def __init__(self, read_by_file=False):
        self.value = 1

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        values = self.reader.values
        if len(values) > 0:
            self.value = values.popleft()

        else:
            self._expected_value("After Skipping must be a value")

    def __str__(self):
        return "SKIPPING= " + str(self.value)
