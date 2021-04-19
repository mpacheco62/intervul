#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .._definitions import _Problem_data


class _Anisotropic_material(_Problem_data):
    pass


class Discontinuous_galerkin(_Anisotropic_material):
    def __str__(self):
        return "DISCONTINUOUS_GALERKIN"
