#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .._definitions import _Problem_data


class _Anisotropic_material(_Problem_data):
    pass


class Fiber_vectors(_Anisotropic_material):
    def __init__(self, read_by_file=False):
        self.value = 2

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        values = self.reader.values
        if len(values) > 0:
            self.value = values.popleft()
        else:
            self._expected_value("After Fiber Vector must be a value")

    def __str__(self):
        return "FIBER_VECTORS= " + str(self.value)
