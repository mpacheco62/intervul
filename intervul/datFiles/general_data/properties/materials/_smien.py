#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Materials


class Smien(_Materials):
    def __init__(self, read_by_file=False):
        # Based on inpgeo.f
        self.imat = 1
        self.density = None
        self.young_modulus = 210.0e3
        self.poisson_ratio = 0.3
        self.free_energy_model = None

        if read_by_file:
            self._init_by_reader()

    def _nextline(self):
        self.reader.next()
        words, values = self.reader.readLikeVulcan()
        return words[0], words, values

    def _init_by_reader(self):
        values = self.reader.values
        value = values.popleft()  # i material
        self.imat = value

        word, words, values = self._nextline()

        if word[:5] == "DENSI":
            self._should_be(word, "DENSITY")
            self.density = values.popleft()
            word, words, values = self._nextline()

        if word[:5] == "YOUNG":
            self._should_be(word, "YOUNG_MODULUS")
            self.young_modulus = values.popleft()
            word, words, values = self._nextline()
        else:
            self._expected(["YOUNG_MODULUS"])

        if word[:5] == "POISS":
            self._should_be(word, "POISSON_RATIO")
            self.poisson_ratio = values.popleft()
            word, words, values = self._nextline()
        else:
            self._expected(["POISSON_RATIO"])

        if word[:5] == "FREE_":
            self._should_be(word, "FREE_ENERGY_MODEL")
            self.free_energy_model = values.popleft()
            word, words, values = self._nextline()

        if word[:5] == "END_M":
            self._should_be(word, "END_MATERIAL")
        else:
            self._expected(["END_MATERIAL"])

    def __str__(self):
        text = "MATERIAL:" + str(self.imat) + ", SMIEN"

        if self.density is not None:
            text += "\n    DENSITY=" + str(self.density)

        text += "\n    YOUNG_MODULUS=" + str(self.young_modulus)
        text += "\n    POISSON_RATIO=" + str(self.poisson_ratio)

        if self.free_energy_model is not None:
            text += "\n    FREE_ENERGY_MODEL=" + str(self.free_energy_model)

        text += "\nEND_MATERIAL\n"
        return text
