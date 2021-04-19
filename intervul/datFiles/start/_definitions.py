#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .._common import Base_dat


class _Start(Base_dat):
    pass


class Sub_start(_Start):
    def __init__(self, read_by_file=False):
        self.timePrev = 0

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        values = self.reader.values
        self.timePrev = values.popleft()

    def __str__(self):
        return "START=" + str(self.timePrev)
