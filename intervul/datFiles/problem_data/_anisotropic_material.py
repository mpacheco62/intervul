#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Problem_data
from .anisotropic_material import Fiber_vectors


class Anisotropic_material(_Problem_data):
    def __init__(self, read_by_file=False):
        self.fiber = None

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words
        if words[1][:5] == "FIBER":
            self._should_be(words[1], "FIBER_VECTORS")
            self.fiber = Fiber_vectors(read_by_file=True)

    def __str__(self):
        text = "ANISOTROPIC_MATERIAL_CONSTITUTIVE_MODELS"
        if self.fiber is not None:
            text += ", " + str(self.fiber)
        return text
