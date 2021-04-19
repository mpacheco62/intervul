#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._common import Base_dat
from .start import (Sub_start,
                    future_analysis,
                    database,
                    Non_standard_initial_cond,
                    new_start,
                    restart)


class Start(Base_dat):
    # Basado en check0.f
    def __init__(self, read_by_file=False):
        self.new_start = new_start.No_initial()
        self.restart = None
        self.start = None
        self.database = None
        self.future_analysis = None
        self.non_standard_initial_cond = None

        if read_by_file:
            self._initByReader(read_by_file=True)

    def _clean_mode_start(self):
        self.new_start = None
        self.restart = None

    def _initByReader(self, **kwargs):
        words = self.reader.words
        word = words.popleft()
        if word[:5] == 'START':
            self._should_be(word, "START")
            self._clean_mode_start()
            self.new_start = new_start.select()

        elif word[:5] == 'RESTA':
            self._should_be(word, "RESTART")
            self._clean_mode_start()
            self.restart = restart.select()

        else:
            self._expected(['START, RESTART'])

        while words:
            word = words.popleft()
            if (word[:5] == "START" and
                    self.new_start is not None and
                    isinstance(self.new_start, new_start.Previous)):

                self._should_be(word, 'START')
                print("WARNING: in line ",
                      self.reader.lineNum(),
                      ", Starting time are defined twice")
                self.start = Sub_start(read_by_file=True)

            elif word[:5] == 'DATAB':
                self._should_be(word, 'DATABASE')
                self.database = database.select()

            elif word[:5] == 'FUTUR':
                self._should_be(word, 'FUTURE_ANALYSIS')
                self.future_analysis = future_analysis.select()

            elif (self.new_start is not None
                  and isinstance(self.new_start, new_start.Initial)
                  and word[:5] == 'NON_S'):
                self._should_be(word, 'NON_STANDARD_INITIAL_COND')
                self.non_standard_initial_cond = (
                                  Non_standard_initial_cond(read_by_file=True))

            else:
                if (self.new_start is not None
                        and isinstance(self.new_start, new_start.Initial)):
                    self._expected(["DATABASE", "FUTURE_ANALYSIS",
                                    "NON_STANDARD_INITIAL_COND"])

                elif (self.new_start is not None
                        and isinstance(self.new_start, new_start.Previous)):
                    self._expected(["START", "DATABASE", "FUTURE_ANALYSIS"])

                else:
                    self._expected(["DATABASE", "FUTURE_ANALYSIS"])

    def __str__(self):
        text = ''
        if self.new_start is not None:
            text += str(self.new_start)
        if self.restart is not None:
            text += str(self.restart)
        if self.start is not None:
            text += ", " + str(self.start)
        if self.database is not None:
            text += ", " + str(self.database)
        if self.future_analysis is not None:
            text += ", " + str(self.future_analysis)
        if self.non_standard_initial_cond is not None:
            text += ", " + str(self.non_standard_initial_cond)
        return text
