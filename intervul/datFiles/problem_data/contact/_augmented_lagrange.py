#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .._definitions import _Problem_data
from .augmented_lagrange import Version


class Augmented_lagrange(_Problem_data):
    def __init__(self, read_by_file=False):
        self.npoic = 0
        self.nnodc = None
        self.version = None

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words
        values = self.reader.values
        word = words.popleft()
        if word[:5] == "NPOIC":  # Number of points of contact
            word = words.popleft()
            self.npoic = values.popleft()

            defined = False
            if word[:5] == "VERSI":
                self._should_be(word, "VERSION")
                self.version = Version(read_by_file=True)
                word = words[0]
                defined = True

            if word[:5] == "NNODC":
                words.popleft()
                word = words[0]
                self.nnodc = values.popleft()
                defined = True

            if not defined:
                self._expected(["VERSION", "NNODC"])

        else:
            self._expected(["NPOIC"])

    def __str__(self):
        text = "AUGMENTED_LAGRANGE, NPOIC:" + str(self.npoic)
        if self.version is not None:
            text += ", " + str(self.version)

        if self.nnodc is not None:
            text += ", NNODC: " + str(self.nnodc)

        return text
