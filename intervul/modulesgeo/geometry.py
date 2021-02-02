#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from . import Reader, Section


def _isInteger(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


def geometryReader(self, problemData):
    line = self.reader.lastLine
    line = line.split(',')
    if len(line) > 1:
        if _isInteger(line[-1]):
            newReader = Reader(self.reader.caseName+'.geo')
            newReader.lastLine = "NO TERMINE CON UNA COMA Y UN ENTERO"
            newFile = Section(newReader,
                              "GEOMETRY",
                              "END_GEOMETRY",
                              geometryReader)
            return newFile(problemData)
    inElement = True
    elements = []
    nodes = []
    for line in self.reader(self.end):
        lineData = line.strip().split()
        if not _isInteger(lineData[1]):
            inElement = False

        if inElement:
            elements.append([int(x) for x in lineData if int(x) != 0])
        else:
            nodes.append([int(lineData[0])] + [float(x) for x in lineData[1:]])

    problemData['nodes'] = nodes
    problemData['elements'] = elements
    if len(nodes) != problemData['NPOIN']:
        print("ADVERTENCIA!!!, La cantidad de nodos leidos (",
              len(nodes),
              ") no concuerdan con los del dat",
              problemData['NPOIN'])
    if len(elements) != problemData['NELEM']:
        print("ADVERTENCIA!!!, La cantidad de elementos (",
              len(elements),
              ") no concuerdan con los del dat",
              problemData['NELEM'])
    return problemData
