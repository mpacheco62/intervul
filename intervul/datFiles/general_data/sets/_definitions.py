#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .._definitions import _General_data


class _Sets(_General_data):
    pass


class Set(_Sets):
    def __init__(self, read_by_file=False):
        self.isets = 1
        self.imats = 1
        self.itype = 30
        self.ntype = 4
        self.irule = 1
        self.igaus = 8
        self.thick = None
        self.isetc = None
        self.imaes = None

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        values = self.reader.values
        self.isets = values.popleft()
        self.imats = values.popleft()
        self.itype = values.popleft()
        self.ntype = values.popleft()
        self.irule = values.popleft()
        self.igaus = values.popleft()

        itype = self.itype
        ntype = self.ntype
        if itype == 30 and (ntype == 1 or ntype == 2 or
                            ntype == 5):
            self.thick = values.popleft()
            if self.thick == 0:
                self._expected(["a thick or area value"])

        if itype == 32:
            self.isetc = values.popleft()
            self.imaes = values.popleft()
            imaes = self.imaes
            thick = values.popleft()

            if thick != 0:
                self.thick = thick

            if imaes == 0:  # old model
                self.thick = self.isetc
                self.isetc = None
                self.imaes = None

    def __str__(self):
        text = "     "
        text += "{} {} {} {} {} {}".format(self.isets,
                                           self.imats,
                                           self.itype,
                                           self.ntype,
                                           self.irule,
                                           self.igaus)

        if self.isetc is not None:
            text += " " + str(self.isetc)

        if self.imaes is not None:
            text += " " + str(self.imaes)

        if self.thick is not None:
            text += " " + str(self.thick)

        return text
