#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Contact
from .non_coincident_mesh import Large_displacements


class Non_coincident_mesh(_Contact):
    def __init__(self, read_by_file=False):
        self.large_displac = None

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words
        word = words[0]

        if word[:5] == "LARGE":
            self._should_be(word, "LARGE_DISPLACEMENTS")
            words.popleft()
            word = words[0]

            self.large_displac = Large_displacements(read_by_file=True)

    def __str__(self):
        text = 'NON_COINCIDENT_MESH'
        if self.large_displac is not None:
            text += ", " + str(self.large_displac)
        return text
