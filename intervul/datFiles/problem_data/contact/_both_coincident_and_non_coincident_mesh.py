#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Contact
from .non_coincident_mesh import Large_displacements


class Both_coincident_and_non_coincident_mesh(_Contact):
    def __init__(self, read_by_file=False):
        self.large_displacements = None

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words
        word = words[0]

        if word[:5] == "LARGE":
            self._should_be(word, "LARGE_DISPLACEMENTS")
            words.popleft()
            word = words[0]

            self.large_displacements = Large_displacements(read_by_file=True)

    def __str__(self):
        text = 'BOTH_COINCIDENT_&_NON_COINCIDENT_MESH'
        if self.large_displacements is not None:
            text += ", " + str(self.large_displacements)
        return text
