#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Intervul
========

Proporciona
  1. Lector de archivos de vulcan
  2. Herramientas para procesar los datos
  3. Objetos que permiten agregar resultados personalizados

La idea de este paquete es tener un libreria basica de entrada y salida de archivos para
vulcan, donde las operaciones complicadas las realice internamente y el usuario solo tenga
que centrarce en como procesar los datos y no como leerlos o escribirlos.

Subpaquetes disponibles
-----------------------
modpyevtk
    Libreria pyevtk modificada para poder agregar vectores y tensores en los resultados

"""

from . import readpos
from .general import ElemTypes, Mesh, AddResults, Results

from ._datFiles import DatFile
from . import datFiles
