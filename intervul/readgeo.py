#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import numpy as np
from intervul.general import ElemTypes, Mesh
from . import modulesgeo as mgeo
from .modulesgeo import Section, Reader
from .modulesgeo.general import _defaultFun

DEBUG = False


def _print(*args):
    if DEBUG:
        print(*args)


class VulcanDat:
    DEBUG = False

    def __init__(self, filename):
        self.end = 'STOP'
        self.reader = Reader(filename)
        rd = self.reader
        self.data = {}
        self.innerSections = [
             Section(rd, "PROBLEM_DATA", "END_PROBLEM", mgeo.problemDataReader),
             Section(rd, "GENERAL_DATA", "END_GENERAL", innerSections=[
                     Section(rd, "GEOMETRY", "END_GEOMETRY", mgeo.geometryReader),
                     Section(rd, "SETS", "END_SETS", mgeo.setsReader),
                     Section(rd, "PROPERTIES", "END_PROPERTIES", innerSections=[
                             Section(rd, "MATERIAL", "END_MATERIAL")
                             ]),
                     ]),
             Section(rd, "INTERVAL_DATA", "END_INTERVAL", innerSections=[
                     Section(rd, "FUNCTION", "END_FUNCTION"),
                     Section(rd, "LOAD", "END_LOAD", innerSections=[
                             ]),
                     Section(rd, "BOUNDARY_DATA", "END_BOUNDARY"),
                     Section(rd, "STRATEGY", "END_STRAT")
                     ])
        ]
        self.data = _defaultFun(self, self.data)
        _print(self.data['SETS'])
        if self.reader.stackOut:
            print("ADVERTENCIA:  no se cerro nunca", self.reader.stackOut[-1])
        self.dataToMesh()

    def dataToMesh(self):
        data = self.data
        elements = data['elements']
        nodes = data['nodes']
        npoin = len(nodes)
        nelem = len(elements)
        mesh = Mesh()
        _print("NNODE", data['NNODE'])
        mesh.ielemFile = np.zeros((nelem), dtype=int)
        mesh.elements = np.zeros((nelem, data['NNODE']), dtype=int)
        mesh.inodeFile = np.empty((npoin), dtype=int)
        mesh.nodes = np.empty((npoin, data['NDIME']), dtype=float)
        mesh.typeElem = np.empty((nelem, 2), dtype=int)
        mesh.elemsSet = np.empty(nelem, dtype=int)

        for elem in elements:
            ielemFile = elem[0]
            ielem = elem[0]-1
            # TODO revisar el 0 based de los sets
            iset = elem[1]
            nnodl = len(elem[2:])
            ntype = data['SETS'][iset]['NTYPE']
            itype = data['SETS'][iset]['ITYPE']
            if (len(data['SETS'][iset]['EXTRA']) <= 1) and (itype == 32):
                nnodl -= 2
            elemType = ElemTypes.getElemType(nnodl, ntype)

            mesh.ielemFile[ielem] = ielemFile
            mesh.elements[ielem, :nnodl] = elem[2:2+nnodl]
            mesh.typeElem[ielem] = [elemType, nnodl]
            mesh.elemsSet[ielem] = iset
        mesh.elements -= 1

        for node in nodes:
            inodeFile = node[0]
            inode = node[0]-1
            mesh.inodeFile[inode] = inodeFile
            mesh.nodes[inode] = node[1:]
        mesh.createiFile()
        self.mesh = mesh
        return mesh
