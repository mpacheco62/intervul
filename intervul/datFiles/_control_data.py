#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from ._common import Base_dat
from .control_data import Postprocess
from .control_data import Renumbering
from .control_data import Cpulimit
from .control_data import Datal
from .control_data import Hourglass
from .control_data import hourglass
from .control_data import smoothing
from .control_data import solver
# from .controlDataBlock import Post_process, Renumbering, Smoothing
# from .controlDataBlock import Cpulimit, Datal, Hourglass
# from .controlDataBlock.solvers import Profile, Frontal, Pcgradient
# from .controlDataBlock.solvers import Gmres, Pardiso


class Control_data(Base_dat):
    # Basado en coninp.f
    def __init__(self, read_by_file=False):
        self.postprocess = None
        self.renumebering = None
        self.smoothing = smoothing.Discrete()
        self.solver = solver.Pardiso()
        self.cpulimit = None
        self.datal = None
        self.hourglass = None

        if read_by_file is not None:
            self._init_by_reader()

    def _init_by_reader(self, **kwargs):
        self.reader.next()
        words, values = self.reader.readLikeVulcan()
        word = words.popleft()
        if word[:5] == 'CONTR':
            self._should_be(word, "CONTROL_DATA")
        else:
            self._expected(['CONTROL_DATA'])

        while True:
            self.reader.next()
            words, values = self.reader.readLikeVulcan()
            word = words[0]

            # 1 coninp.f
            if word[:5] == "POSTP":
                self._should_be(word, "POSTPROCESS")
                self.postprocess = Postprocess()

            elif word[:5] == "RENUM":
                self._should_be(word, "RENUMBERING")
                self.renumebering = Renumbering()

            elif word[:5] == "SMOOT":
                self._should_be(word, "SMOOTHING")
                self.smoothing = smoothing.select()

            elif word[:5] == 'SOLVE':
                self._should_be(word, "SOLVER")
                word = words[1]

                if word[:5] == "PROFI":
                    self._should_be(word, "PROFILE")
                    self.solver = solver.Profile(read_by_file=True)

                elif word[:5] == "FRONT":
                    self._should_be(word, "FRONTAL")
                    self.solver = solver.Frontal(read_by_file=True)

                elif word[:5] == "PCGRA":
                    self._should_be(word, "PCGRADIENT")
                    self.solver = solver.Pcgradient(read_by_file=True)

                elif word[:5] == "GMRES":
                    self._should_be(word, "GMRES")
                    self.solver = solver.Gmres(read_by_file=True)

                elif word[:5] == "PARDI":
                    self._should_be(word, "PARDISO")
                    self.solver = solver.Pardiso(read_by_file=True)
                else:
                    self._expected(["PROFILE", "FRONTAL", "PCGRADIENT",
                                    "GMRES", "PARDISO"])

            elif word[:5] == "CPULI":
                self._should_be(word, "CPULIMIT")
                self.cpulimit = Cpulimit(read_by_file=True)

            elif word[:5] == "DATAL":
                self._should_be(word, "TODO SEARCH REAL VALUE")
                self.datal = Datal(read_by_file=True)

            elif word[:5] == "HOURG":
                self._should_be(word, "HOURGLASS")
                self.hourglass = Hourglass(read_by_file=True)

            elif word[:5] == "END_C":
                self._should_be(word, "END_CONTROL_DATA")
                break

            else:
                self._expected(["POSTPROCESS", "RENUMBERING", "SMOOTHING",
                                "END_CONTROL_DATA"])

    def __str__(self):
        text = 'CONTROL_DATA\n'
        if self.postprocess is not None:
            text += str(self.postprocess) + "\n"

        if self.renumebering is not None:
            text += str(self.renumebering) + "\n"

        if self.smoothing is not None:
            text += str(self.smoothing) + "\n"

        if self.solver is not None:
            text += str(self.solver) + "\n"

        if self.cpulimit is not None:
            text += str(self.cpulimit) + "\n"

        # if self.datal is not None:
        #     text += str(self.datal) + "\n"

        if self.hourglass is not None:
            text += str(self.hourglass) + "\n"

        text += 'END_CONTROL_DATA'

        return text
