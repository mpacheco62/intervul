#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function


def setsReader(self, problemData):
    setsData = {}
    for line in self.reader(self.end):
        lineData = line.split()
        setData = {'IMATS': int(lineData[1]),
                   'ITYPE': int(lineData[2]),
                   'NTYPE': int(lineData[3]),
                   'IRULE': int(lineData[4]),
                   'IGAUS': int(lineData[5])
                   }
        if len(lineData) > 6:
            setData['EXTRA'] = lineData[6:]
        else:
            setData['EXTRA'] = []
        setsData[int(lineData[0])] = setData
    problemData['SETS'] = setsData
    return problemData
