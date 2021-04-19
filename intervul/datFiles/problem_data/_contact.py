#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Problem_data
from .contact import Augmented_lagrange, Non_coincident_mesh


class Contact(_Problem_data):
    def __init__(self, read_by_file=False):
        self.augmented_lagrange = None
        self.non_coincident_mesh = None

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        words = self.reader.words

        words.popleft()  # Contact word
        word = words[0]
        if word[:5] == "AUGME":
            self._should_be(word, "AUGMENTED_LAGRANGE")
            words.popleft()
            self.augmented_lagrange = Augmented_lagrange(
                                         read_by_file=True)
            word = words[0]  # Augmented.. cambia las words

        if word[:5] == "NON_C":
            self._should_be(word, "NON_COINCIDENT_MESH")
            words.popleft()
            word = words[0]
            self.non_coincident_mesh = Non_coincident_mesh(
                                        read_by_file=True)

    def __str__(self):
        text = "CONTACT"
        if self.augmented_lagrange is not None:
            text += ", " + str(self.augmented_lagrange)

        if self.non_coincident_mesh is not None:
            text += ", " + str(self.non_coincident_mesh)

        return text




