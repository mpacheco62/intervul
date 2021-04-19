#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .._common import Base_dat


class _Problem_data(Base_dat):
    pass


class Seepage(_Problem_data):
    def __str__(self):
        return "SEEPAGE"


class Structural_continuum(_Problem_data):
    def __str__(self):
        return "STRUCTURAL,CONTINUUM"


class Structural_shells(_Problem_data):
    def __str__(self):
        return "STRUCTURAL,SHELLS"


class Waves(_Problem_data):
    def __str__(self):
        return "WAVES"


class Thermal(_Problem_data):
    def __str__(self):
        return "THERMAL"


class Incompressibility(_Problem_data):
    def __str__(self):
        return "INCOMPRESSIBILITY"


class Dynamic(_Problem_data):
    def __str__(self):
        return "DYNAMIC"


class Coupl(_Problem_data):
    def __str__(self):
        return "COUPL"


class Dimensions(_Problem_data):
    def __init__(self, read_by_file=False):
        self.npoin = 8
        self.nelem = 1
        self.ndime = 3
        self.nnode = 8
        self.ngaus = 8
        self.nsets = 1
        self.nmats = 1
        self.nfunc = 1

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words
        values = self.reader.values
        words.popleft()  # dimen word

        while words:
            word = words.popleft()
            value = values.popleft()

            if word[:5] == "NPOIN":
                self.npoin = value

            elif word[:5] == "NELEM":
                self.nelem = value

            elif word[:5] == "NDIME":
                self.ndime = value

            elif word[:5] == "NNODE":
                self.nnode = value

            elif word[:5] == "NGAUS":
                self.ngaus = value

            elif word[:5] == "NSETS":
                self.nsets = value

            elif word[:5] == "NMATS":
                self.nmats = value

            elif word[:5] == "NFUNC":
                self.nfunc = value

            else:
                self._expected(["NPOIN", "NELEM", "NDIME", "NNODE",
                                "NGAUS", "NSETS", "NMATS", "NFUNC"])

    def __str__(self):
        text = ("DIMENSIONS: NPOIN={:6d}, NELEM={:6d}, "
                "NDIME={:2d}, NNODE={:2d} \\\n"
                "            NGAUS={:6d}, NSETS={:6d}, "
                "NMATS={:2d}, NFUNC={:2d}")
        text = text.format(self.npoin, self.nelem, self.ndime, self.nnode,
                           self.ngaus, self.nsets, self.nmats, self.nfunc)
        return text


class Local_coordinate_system(_Problem_data):
    def __init__(self, read_by_file=False):
        self.value = 1

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        values = self.reader.values
        if len(values) > 0:
            self.value = values.popleft()
        else:
            self._expected_value("After Local Cordinate System"
                                 " must be a value")

    def __str__(self):
        return "LOCAL_COORDINATE_SYSTEM= " + str(self.value)


class Active_elements(_Problem_data):
    def __str__(self):
        return "ACTIVE_ELEMENTS"


class Deformation_dependent_face_load(_Problem_data):
    def __str__(self):
        return "DEFORMATION_DEPENDENT_FACE_LOAD"
