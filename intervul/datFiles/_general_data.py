#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ._common import Base_dat
from .general_data import Geometry, Sets, Properties


class General_data(Base_dat):
    # Basado en inpdat.f
    def __init__(self, read_by_file=False):
        self.geometry = None
        self.properties = None
        self.tuning_parameters = None
        self.sets = None
        self.free_parameters = None
        self.contact = None

        if read_by_file:
            self._init_by_reader()

    def _init_by_reader(self):
        self.reader.next()
        words, values = self.reader.readLikeVulcan()

        word = words[0]
        if word[:5] == 'GENER':
            self._should_be(word, "GENERAL_DATA")
        else:
            self._expected(["GENERAL_DATA"])

        while True:
            self.reader.next()
            words, values = self.reader.readLikeVulcan()
            word = words[0]

            if word[:5] == "GEOME":
                self._should_be(word, "GEOMETRY")
                self.geometry = Geometry(read_by_file=True)

            elif word[:5] == "PROPE":
                self._should_be(word, "PROPERTIES")
                self.properties = Properties(read_by_file=True)

            # elif word[:5] == "TUNIN":
            #     self._should_be(word, "TUNING_PARAMETERS")
            #     self.type = Tuning_parameters()

            elif word[:4] == "SETS":
                self._should_be(word, "SETS")
                self.sets = Sets(read_by_file=True)

            # elif word[:5] == "FREE_":
            #     self._should_be(word, "FREE_")
            #     self.type = Free_()

            # elif word[:5] == "CONTA":
            #     self._should_be(word, "CONTACT_PARAMETERS")
            #     self.dynamic = Contact_parameters()

            elif word[:5] == "END_G":
                self._should_be(word, "END_GENERAL_DATA")
                break

            else:
                pass
                # self._expected(["GEOMETRY",
                #                 "PROPERTIES",
                #                 "TUNING_PARAMETERS",
                #                 "SETS",
                #                 "FREE_",
                #                 "CONTACT_PARAMETERS",
                #                 "END_GENERAL_DATA"])

    def __str__(self):
        text = "GENERAL_DATA"

        if self.geometry is not None:
            text += "\n" + str(self.geometry)

        if self.sets is not None:
            text += "\n" + str(self.sets)

        if self.properties is not None:
            text += "\n" + str(self.properties)

        # if self.dynamic is not None:
        #     text += "\n" + str(self.dynamic)

        # if self.coupl is not None:
        #     text += "\n" + str(self.coupl)

        # if self.large_strain_disp is not None:
        #     text += "\n" + str(self.large_strain_disp)

        # text += "\n" + str(self.dimensions)

        # if self.contact is not None:
        #     text += "\n" + str(self.contact)

        # if self.local_coordinate_system is not None:
        #     text += "\n" + str(self.local_coordinate_system)

        # if self.active_elements is not None:
        #     text += "\n" + str(self.active_elements)

        # if self.deformation_dependent_face_load is not None:
        #     text += "\n" + str(self.deformation_dependent_face_load)

        # if self.anisotropic_material is not None:
        #     text += "\n" + str(self.anisotropic_material)

        # if self.weak_form is not None:
        #     text += "\n" + str(self.weak_form)

        text += "\n" + "END_GENERAL_DATA"
        return text
