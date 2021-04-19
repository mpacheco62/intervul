#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import _Control_data


class _Solver(_Control_data):
    def __init__(self, words, values):
        self.name = ""

    def toPrintValues(self, order):
        toPrint = dict()
        skip = True
        for name, value in reversed(order):
            if value != 0:
                skip = False
            if skip:
                toPrint[name] = False
            else:
                toPrint[name] = True

        return toPrint


class Profile(_Solver):
    def __init__(self, read_by_file=False):
        self.symmetry = 0
        self.nwidth = 0
        self.mitcg = 0
        self.tolcg = 0
        self.tolc1 = 0

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        values = self.reader.values
        # posible values: 0, 1 and 2 (on skyass.f)
        self.symmetry = values[0]

        # banda del profile, si es 0 representa 50000 en vulcan
        self.nwidth = values[1]

        # 0 hace backsolution y 1 hace iterative solution
        self.mitcg = values[2]

        # alguna tolerancia del metodo
        self.tolcg = values[3]

        # alguna tolerancia del metodo
        self.tolc1 = values[4]

    def __str__(self):
        checkToPrint = self.toPrintValues([("symmetry", self.symmetry),
                                           ("nwidth", self.nwidth),
                                           ("mitcg", self.mitcg),
                                           ("tolcg", self.tolcg),
                                           ("tolc1", self.tolc1)
                                           ])
        text = "SOLVER, PROFILE"
        if checkToPrint["symmetry"]:
            text += ": " + str(self.symmetry)

        if checkToPrint["nwidth"]:
            text += ", " + str(self.nwidth)

        if checkToPrint["mitcg"]:
            text += ", " + str(self.mitcg)

        if checkToPrint["tolcg"]:
            text += ", " + str(self.tolcg)

        if checkToPrint["tolc1"]:
            text += ", " + str(self.tolc1)

        return text


class Frontal(_Solver):
    def __init__(self, read_by_file=False):
        self.symmetry = 0
        self.nbufa = 0
        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        values = self.reader.values
        # posible values: 0, 1 and 2 (on skyass.f)
        self.symmetry = values[0]

        # nbufa
        self.nbufa = values[1]

    def __str__(self):
        checkToPrint = self.toPrintValues([("symmetry", self.symmetry),
                                           ("nbufa", self.nbufa),
                                           ])
        text = "SOLVER, FRONTAL"
        if checkToPrint["symmetry"]:
            text += ": " + str(self.symmetry)

        if checkToPrint["nbufa"]:
            text += ", " + str(self.nbufa)

        return text


class Pcgradient(_Solver):
    def __init__(self, read_by_file=False):
        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        words = self.reader.words
        values = self.reader.values
        # Numero de iteraciones maximas
        self.mitcg = values[0]

        # Tolerancia
        self.tolcg = values[1]

        # Es un tema con la memoria, creo que con 0 guarda parte de
        # la memoria y con -1 la memoria entera
        if values[2] == 0:
            self.nwidth = 0
        else:
            self.nwidth = -1

        self.tolc1 = values[3]

        if words[2][:5] == 'PRINT':
            self.nprir = 1
        else:
            self.nprir = 0

    def __str__(self):
        checkToPrint = self.toPrintValues([
                                           ("mitcg", self.mitcg),
                                           ("tolcg", self.tolcg),
                                           ("nwidth", self.nwidth),
                                           ("tolc1", self.tolc1)
                                           ])
        text = "SOLVER, PCGRADIENT"
        if checkToPrint["mitcg"]:
            text += ": " + str(self.mitcg)

        if checkToPrint["tolcg"]:
            text += ", " + str(self.tolcg)

        if checkToPrint["nwidth"]:
            text += ", " + str(self.nwidth)

        if checkToPrint["tolc1"]:
            text += ", " + str(self.tolc1)

        return text


class Pardiso(_Solver):
    def __init__(self, read_by_file=False):
        self.symmetry = 0
        self.nthreads = 0
        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        values = self.reader.values
        self.symmetry = values[0]
        self.nthreads = values[1]

    def __str__(self):
        checkToPrint = self.toPrintValues([("symmetry", self.symmetry),
                                           ("nthreads", self.nthreads),
                                           ])
        text = "SOLVER, PARDISO"
        if checkToPrint["symmetry"]:
            text += ": " + str(self.symmetry)

        if checkToPrint["nthreads"]:
            text += ", " + str(self.nthreads)

        return text


class Gmres(_Solver):
    def __init__(self, read_by_file=False):
        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        values = self.reader.values
        # Numero de iteraciones maximas
        self.mitcg = values[0]

        # Tolerancia
        self.tolcg = values[1]

        # No se
        self.mkryl = values[2]

        # Tampoco se
        self.ipgmr = values[3]

    def __str__(self):
        checkToPrint = self.toPrintValues([
                                           ("mitcg", self.mitcg),
                                           ("tolcg", self.tolcg),
                                           ("mkryl", self.mkryk),
                                           ("ipgmr", self.ipgmr)
                                           ])
        text = "SOLVER, GMRES"
        if checkToPrint["mitcg"]:
            text += ", " + str(self.mitcg)

        if checkToPrint["tolcg"]:
            text += ", " + str(self.tolcg)

        if checkToPrint["mkryl"]:
            text += ", " + str(self.mkryl)

        if checkToPrint["ipgmr"]:
            text += ", " + str(self.ipgmr)
        return text
