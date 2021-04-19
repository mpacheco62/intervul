#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Properties
from .materials._definitions import _Materials
from .materials import Smien


class Materials(_Properties):
    def __init__(self, read_by_file=False):
        # based on inpset.f
        self.data = []
        self.data.append(Smien())

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words
        values = self.reader.values

        self.data = []
        while True:
            if words[0][:5] == "MATER" and words[0][:9] != "MATERIAL_":
                self._should_be(words[0], "MATERIAL")
                if words[1] == "SMIEN":
                    self.data.append(Smien(read_by_file=True))
                    self.reader.next()
                    words, values = self.reader.readLikeVulcan()

            else:
                break

    def __str__(self):
        text = ''
        for imat in self.data:
            text += str(imat)

        return text

    def __len__(self):
        return self.data.len()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        if isinstance(value, _Materials):
            self.data[key] = value
        else:
            raise TypeError("Expected Materials type on assignment")

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return self.data.iter()

    def __reversed__(self):
        return self.data.__reversed__()
