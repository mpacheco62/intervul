#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Problem_data
from .weak_form import Discontinuous_galerkin


class Weak_form(_Problem_data):
    def __init__(self, read_by_file=False):
        self.discontinuous = None

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words
        if words[1][:5] == "DISCO":
            self._should_be(words[1], "DISCONTINUOUS_GALERKIN")
            self.discontinuous = Discontinuous_galerkin()

        else:
            self._expected(["DISCONTINUOUS_GALERKIN"])

    def __str__(self):
        return "WEAK_FORM, " + str(self.discontinuous)
