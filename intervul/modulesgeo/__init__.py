#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
modulesgeo
========

Proporciona
  1. Funciones para leer partes especificas de los archivos geo de vulcan

La idea de este paquete es tener un libreria basica de entrada y salida de archivos para
vulcan, donde las operaciones complicadas las realice internamente y el usuario solo tenga
que centrarce en como procesar los datos y no como leerlos o escribirlos.

"""
from .problemData import problemDataReader
from .general import Reader, Section
from .geometry import geometryReader
from .sets import setsReader
