#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._definitions import _Problem_data


class _Large_strain_disp(_Problem_data):
    pass


class Total_langragian(_Large_strain_disp):
    def __str__(self):
        return "LARGE_STRAINS_&_DISPLACEMENTS: TOTAL_LAGRANGIAN"


class Updated_langragian(_Large_strain_disp):
    def __str__(self):
        return "LARGE_STRAINS_&_DISPLACEMENTS: UPDATED_LAGRANGIAN"


class Eulerian_form(_Large_strain_disp):
    def __str__(self):
        return "LARGE_STRAINS_&_DISPLACEMENTS: EULERIAN_FORM"


def select():
    instance = _Large_strain_disp()
    words = instance.reader.words

    if words[1] != " ":
        word = words[1]
        if word[:5] == "TOTAL":   # default
            instance._should_be(word, "TOTAL_LAGRANGIAN")
            return Total_langragian()

        elif word[:5] == "UPDAT":
            instance._should_be(word, "UPDATED_LAGRANGIAN")
            return Updated_langragian()

        elif word[:5] == "EULER":
            instance._should_be(word, "EULERIAN_FORM")
            return Eulerian_form()

    else:
        return Total_langragian()
