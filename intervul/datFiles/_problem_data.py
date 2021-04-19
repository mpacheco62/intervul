#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._common import Base_dat
from .problem_data import (Seepage,
                           Structural_continuum,
                           Structural_shells,
                           Waves,
                           Thermal,
                           Incompressibility,
                           Dynamic,
                           Coupl,
                           Dimensions,
                           Contact,
                           Local_coordinate_system,
                           Active_elements,
                           Deformation_dependent_face_load,
                           Anisotropic_material,
                           Weak_form)
from . import problem_data


class Problem_data(Base_dat):
    # Basado en proinp.f
    def __init__(self, read_by_file=False):
        self.type = None
        self.dynamic = None
        self.coupl = None
        self.large_strain_disp = None
        self.dimensions = Dimensions()
        self.contact = None
        self.local_coordinate_system = None
        self.active_elements = None
        self.deformation_dependent_face_load = None
        self.anisotropic_material = None
        self.weak_form = None

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        self.reader.next()
        words, values = self.reader.readLikeVulcan()

        word = words[0]
        if word[:5] == 'PROBL':
            self._should_be(word, "PROBLEM_DATA")
        else:
            self._expected(["PROBLEM_DATA"])

        while True:
            self.reader.next()
            words, values = self.reader.readLikeVulcan()
            word = words[0]

            if word[:5] == "SEEPA":
                self._should_be(word, "SEEPAGE")
                self.type = Seepage()

            elif word[:5] == "STRUC":
                self._should_be(word, "STRUCTURAL")
                if words[1][:5] == "CONTI":
                    self._should_be(words[1], "CONTINUUM")
                    self.type = Structural_continuum()

                elif words[1][:5] == "SHELL":
                    self._should_be(words[1], "SHELLS")
                    self.type = Structural_shells()

                else:
                    self.type = Structural_continuum()

            elif word[:5] == "WAVES":
                self._should_be(word, "WAVES")
                self.type = Waves()

            elif word[:5] == "THERM":
                self._should_be(word, "THERMAL")
                self.type = Thermal()

            elif word[:5] == "INCOM":
                self._should_be(word, "INCOMPRESSIBILITY")
                self.type = Incompressibility()

            elif word[:5] == "DYNAM":
                self._should_be(word, "DYNAMIC")
                self.dynamic = Dynamic()

            elif word[:5] == "COUPL":
                self._should_be(word, "COUPL")
                self.coupl = Coupl()

            elif word[:5] == "LARGE":
                self._should_be(word, "LARGE_STRAINS_&_DISPLACEMENTS")
                self.large_strain_disp = problem_data.large_strain_disp.select()

            elif word[:5] == "DIMEN":
                self._should_be(word, "DIMENSIONS")
                self.dimensions = Dimensions(read_by_file=True)

            elif word[:5] == "CONTA":
                self._should_be(word, "CONTACT")
                self.contact = Contact(read_by_file=True)

            elif word[:5] == "LOCAL":
                self._should_be(word, "LOCAL_COORDINATE_SYSTEM")
                self.local_coordinate_system = Local_coordinate_system(
                                                            read_by_file=True)

            elif word[:5] == "ACTIV":
                self._should_be(word, "ACTIVE_ELEMENTS")
                self.active_elements = Active_elements()

            elif word[:5] == "DEFOR":
                self._should_be(word, "DEFORMATION_DEPENDENT_FACE_LOAD")
                self.deformation_dependent_face_load = (
                                                Deformation_dependent_face_load())

            elif word[:5] == "ANISO":
                self._should_be(word, "ANISOTROPIC_MATERIAL_"
                                     "CONSTITUTIVE_MODELS")
                self.anisotropic_material = Anisotropic_material(
                                                            read_by_file=True)

            elif word[:5] == "WEAK_":
                self._should_be(word, "WEAK_FORM")
                self.weak_form = Weak_form(read_by_file=True)

            elif word[:5] == "END_P":
                self._should_be(word, "END_PROBLEM_DATA")
                break

            else:
                self._expected(["SEEPAGE",
                                "STRUCTURAL",
                                "WAVES",
                                "THERMAL",
                                "INCOMPRESSIBILITY",
                                "DYNAMIC",
                                "COUPL",
                                "LARGE_STRAINS_&_DISPLACEMENTS",
                                "DIMENSIONS",
                                "CONTACT",
                                "LOCAL_COORDINATE_SYSTEM",
                                "ACTIVE_ELEMENTS",
                                "DEFORMATION_DEPENDENT_FACE_LOAD",
                                "ANISOTROPIC_MATERIAL_CONSTITUTIVE_MODELS",
                                "WEAK_FORM",
                                "END_PROBLEM_DATA"])

    def __str__(self):
        text = "PROBLEM_DATA"

        if self.type is not None:
            text += "\n" + str(self.type)

        if self.dynamic is not None:
            text += "\n" + str(self.dynamic)

        if self.coupl is not None:
            text += "\n" + str(self.coupl)

        if self.large_strain_disp is not None:
            text += "\n" + str(self.large_strain_disp)

        text += "\n" + str(self.dimensions)

        if self.contact is not None:
            text += "\n" + str(self.contact)

        if self.local_coordinate_system is not None:
            text += "\n" + str(self.local_coordinate_system)

        if self.active_elements is not None:
            text += "\n" + str(self.active_elements)

        if self.deformation_dependent_face_load is not None:
            text += "\n" + str(self.deformation_dependent_face_load)

        if self.anisotropic_material is not None:
            text += "\n" + str(self.anisotropic_material)

        if self.weak_form is not None:
            text += "\n" + str(self.weak_form)

        text += "\n" + "END_PROBLEM_DATA"
        return text
