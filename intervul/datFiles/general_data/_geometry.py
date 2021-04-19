#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _General_data
from .._common import _Reader
from .geometry import Interpolate, Noninterpolate
import os


class Geometry(_General_data):
    def __init__(self, read_by_file=False):
        # Based on inpgeo.f
        self.interpolate = None
        self.onDat = True
        self.elements = [[1, 1, 1, 2, 3, 4, 5, 6, 7, 8]]
        self.nodes = [[1, 0.0, 0.0, 0.0],
                      [2, 1.0, 0.0, 0.0],
                      [3, 1.0, 1.0, 0.0],
                      [4, 0.0, 1.0, 0.0],
                      [5, 0.0, 0.0, 1.0],
                      [6, 1.0, 0.0, 1.0],
                      [7, 1.0, 1.0, 1.0],
                      [8, 0.0, 1.0, 1.0]]

        self.origianlReader = self.reader

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words
        word = words.popleft()  # GEOMETRY
        word = words.popleft()  # INTERPOLATE OR NOT
        values = self.reader.values
        value = values.popleft()  # CODE TO GEO IF EXIST

        self.elements = []
        self.nodes = []

        if word[:5] == "INTER":
            self._should_be(word, "INTERPOLATE")
            self.interpolate = Interpolate()
        else:
            self._should_be(word, "NONINTERPOLATE")
            self.interpolate = Noninterpolate()

        if value != 0:
            self.onDat = False
            caseName = self.reader.caseName
            dirname = self.reader.dirname
            geo_filename = os.path.join(dirname, caseName + ".geo")
            self.reader = _Reader(geo_filename)

        onElements = True
        firstElement = True
        line = self.reader.next()
        while not line.strip().startswith("END_G"):
            if onElements:
                ielem = int(line.strip().split()[0])
                if ielem == 1 and (not firstElement):
                    onElements = False
                else:
                    element = [int(val) for val in line.split()]  # A enteros
                    self.elements.append(element)
                    firstElement = False

            if not onElements:
                node = [float(val) for val in line.split()]  # A flotante
                node[0] = int(node[0])  # Numero de nodo
                self.nodes.append(node)
            try:
                line = self.reader.next()
            except StopIteration:
                break

        if not self.onDat:
            self.origianlReader.next()
            self.reader = self.origianlReader

        words, values = self.reader.readLikeVulcan()
        self._should_be(words[0], "END_GEOMETRY")

    def __str__(self):
        text = "GEOMETRY," + str(self.interpolate)
        if not self.onDat:
            text += ",140"
        text += "\n"

        for elem in self.elements:
            text += ' '.join('{:7d}'.format(val) for val in elem)
            text += "\n"

        for node in self.nodes:
            text += "{:7d}".format(node[0])
            text += ' '.join('{:15.7E}'.format(val) for val in node[1:])
            text += "\n"

        text += "END_GEOMETRY"
        return text
