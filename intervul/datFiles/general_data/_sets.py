#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _General_data
from .._common import _Reader
from .sets import Set
from .sets._definitions import _Sets
import os


class Sets(_General_data):
    def __init__(self, read_by_file=False):
        # based on inpset.f
        self.data = []
        self.data.append(Set())
        self.onDat = True

        self._originalReader = self.reader

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words
        words.popleft()  # SETS
        values = self.reader.values
        value = values.popleft()  # CODE TO SET FILE IF EXIST (141)

        self.data = []

        if value != 0:
            self.onDat = False
            caseName = self.reader.caseName
            dirname = self.reader.dirname
            set_filename = os.path.join(dirname, caseName + ".set")
            self.reader = _Reader(set_filename)
            _Sets.reader = self.reader

        self.reader.next()
        words, values = self.reader.readLikeVulcan()
        while words[0][:5] != "END_S":
            self.data.append(Set(read_by_file=True))
            try:
                self.reader.next()
                words, values = self.reader.readLikeVulcan()
            except StopIteration:
                break

        if not self.onDat:
            self._originalReader.next()
            self.reader = self._originalReader
            _Sets.reader = self.reader

        words, values = self.reader.readLikeVulcan()
        self._should_be(words[0], "END_SETS")

    def __str__(self):
        text = "SETS"
        if not self.onDat:
            text += ",141"
        text += "\n"

        for iset in self.data:
            text += '    ' + str(iset)
            text += "\n"

        text += "END_SETS"
        return text

    def __len__(self):
        return self.data.len()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        if isinstance(value, Set):
            self.data[key] = value
        else:
            raise TypeError("Expected Set type on assignment")

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return self.data.iter()

    def __reversed__(self):
        return self.data.__reversed__()
