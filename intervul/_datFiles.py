#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .datFiles import _Reader, Base_dat, Start, Control_data, Problem_data
from .datFiles import General_data
# from totest.control_data import Control_data


class DatFile:
    def __init__(self, filename):
        self.reader = _Reader(filename)
        Base_dat.reader = self.reader
        for line in self.reader:
            if line.startswith("VULCAN"):
                self.title = line.strip().split(':')[1]
                break

        self.reader.next()
        self.reader.readLikeVulcan()
        self.start = Start(read_by_file=True)
        self.control_data = Control_data(read_by_file=True)
        self.problem_data = Problem_data(read_by_file=True)
        self.general_data = General_data(read_by_file=True)

    def __str__(self):
        text = str(self.start)
        text += "\n" + str(self.control_data)
        text += "\n" + str(self.problem_data)
        text += "\n" + str(self.general_data)

        return text
