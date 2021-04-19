#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Non_coincident_mesh
from .large_displacements import Non_linearized, Maximum_gap, Skipping


class Large_displacements(_Non_coincident_mesh):
    def __init__(self, read_by_file=False):
        self.non_linearized = None
        self.maximum_gap = None
        self.skipping = None

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words
        word = words[0]

        if word[:5] == "NON_L":
            self._should_be(word, "NON_LINEARIZED_COMPUTATION_OF_N")
            words.popleft()
            word = words[0]

            self.non_linearized = Non_linearized(read_by_file=True)

        if word[:5] == "MAXIM":
            self._should_be(word, "MAXIMUM_GAP_FOR_POSSIBLE_CONTACT")
            words.popleft()
            word = words[0]

            self.maximum_gap = Maximum_gap(read_by_file=True)

        if word[:5] == "SKIPP":
            self._should_be(word, "SKIPPING")
            words.popleft()
            word = words[0]

            self.skipping = Skipping(read_by_file=True)

    def __str__(self):
        text = "LARGE_DISPLACEMENTS"
        if self.non_linearized is not None:
            text += ",\\\n " + str(self.non_linearized)

        if self.maximum_gap is not None:
            text += ",\\\n " + str(self.maximum_gap)

        if self.skipping is not None:
            text += ",\\\n " + str(self.skipping)

        return text
