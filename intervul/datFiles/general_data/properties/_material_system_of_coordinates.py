#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Properties


class Material_system_of_coordinates(_Properties):
    def __init__(self, read_by_file=False):
        # based on inpset.f
        self.data = []
        self.data.append([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words
        values = self.reader.values

        self.data = []

        line = self.reader.next()  # jump MATERIAL_SYSTEM...
        words, values = self.reader.readLikeVulcan()
        word = words[0]
        ndata = values[0]

        while word[:5] != "END_M":
            temp = line.split()
            temp[0] = int(temp[0])
            temp[1:] = [float(val) for val in temp[1:]]
            self.data.append(temp)
            self.reader.next()
            words, values = self.reader.readLikeVulcan()
            word = words[0]

        self._should_be(word, "END_MATERIAL_SYSTEM_OF_COORDINATES")

        if ndata != len(self.data):
            raise ValueError(str(ndata) + "not match to elements" +
                             str(len(self.data)))

    def __str__(self):
        text = 'MATERIAL_SYSTEM_OF_COORDINATES\n'
        text += "{:7d}\n".format(len(self.data))

        for ielem in self.data:
            text += "{:7d}".format(ielem[0]) + " "
            text += ' '.join('{:9.7F}'.format(val) for val in ielem[1:])
            text += "\n"

        text += "END_MATERIAL_SYSTEM_OF_COORDINATES"
        return text

    def __len__(self):
        return self.data.len()

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return self.data.iter()

    def __reversed__(self):
        return self.data.__reversed__()
