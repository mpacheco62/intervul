#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _General_data
from .._common import _Reader
# from .properties import Set
from .properties._definitions import _Properties
from .properties import Materials, Material_system_of_coordinates
import os


class Properties(_General_data):
    def __init__(self, read_by_file=False):
        # based on inppro.f
        self.materials = Materials()
        self.material_system_of_coordinates = None
        self.onDat = True

        self._originalReader = self.reader

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words
        words.popleft()  # PROPERTIES
        values = self.reader.values
        value = values.popleft()  # CODE TO MAT FILE IF EXIST (142)

        if value != 0:
            self.onDat = False
            caseName = self.reader.caseName
            dirname = self.reader.dirname
            set_filename = os.path.join(dirname, caseName + ".mat")
            self.reader = _Reader(set_filename)
            _Properties.reader = self.reader

        self.reader.next()
        words, values = self.reader.readLikeVulcan()
        self.materials = Materials(read_by_file=True)

        self.reader.next()
        words, values = self.reader.readLikeVulcan()
        self.material_system_of_coordinates = Material_system_of_coordinates(
                                                             read_by_file=True)

        if not self.onDat:
            self.reader = self._originalReader
            _Properties.reader = self.reader

        self._originalReader.next()
        words, values = self.reader.readLikeVulcan()
        if words[0][:5] != "END_P":
            self._expected(['END_PROPERTIES'])
        self._should_be(words[0], "END_PROPERTIES")

    def __str__(self):
        text = "PROPERTIES"
        if not self.onDat:
            text += ",142"
        text += "\n"

        text += str(self.materials)
        text += str(self.material_system_of_coordinates)
        text += "END_PROPERTIES"
        return text
