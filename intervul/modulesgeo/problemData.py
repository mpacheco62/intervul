#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import re


def problemDataReader(self, problemData):
    for line in self.reader(self.end):
        if line.startswith("DIMENSIONS"):
            line = line.split(':')[1].strip()

            # Se eliminan los posibles espacios entre el igual y el numero
            line = "=".join([x.strip() for x in line.split('=')])

            # Ahora se separan los datos, por coma y espacios
            lineData = re.split('[, ]+', line)
            for key, data in [tuple(text.split('=')) for text in lineData]:
                problemData[key] = int(data)
    return problemData
