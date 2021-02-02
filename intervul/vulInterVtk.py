#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import numpy as np
from intervul.readgeo import VulcanDat
from intervul.general import ElemTypes
from intervul.modpyevtk.vtk import  VtkVertex,VtkPolyVertex,VtkLine,VtkPolyLine,VtkTriangle,VtkTriangleStrip,VtkPolygon,VtkPixel,VtkQuad,VtkTetra,VtkVoxel,VtkHexahedron,VtkWedge,VtkPyramid,VtkQuadraticEdge,VtkQuadraticTriangle,VtkQuadraticQuad,VtkQuadraticTetra,VtkQuadraticHexahedron


def vulcanType2vtk(itype):
  if itype == ElemTypes.HEXA8:  return VtkHexahedron.tid
  if itype == ElemTypes.HEXA20: return VtkQuadraticHexahedron.tid
  if itype == ElemTypes.TETR4:  return VtkTetra.tid
  if itype == ElemTypes.TETR10: return VtkQuadraticTetra.tid
  if itype == ElemTypes.TOBL6:  return VtkWedge.tid
  if itype == ElemTypes.TRIA3:  return VtkTriangle.tid
  if itype == ElemTypes.TRIA6:  return VtkQuadraticTriangle.tid
  if itype == ElemTypes.QUAD4:  return VtkQuad.tid
  if itype == ElemTypes.QUAD8:  return VtkQuadraticQuad.tid
  if itype == ElemTypes.LINE2:  return VtkLine.tid
  raise TypeError("Elemento Desconocido",itype)

def meshToVtkFormat(mesh):
  submeshs = mesh.splitMeshBySet()
  nsets = len(submeshs)

  for iset,mesh in submeshs.items():
    nodes = mesh.nodes3d()
#    print(nodes)
    mesh.splitCoordinates()

    nelem, nnode      = mesh.elements.shape
    mesh.connectivity = np.empty(nelem*nnode, dtype=int)
    mesh.offset       = np.empty(nelem, dtype=int)
    mesh.ctype        = np.empty(nelem, dtype=int)
  
    index = 0
    for ielem, (typeElem, element) in enumerate(zip(mesh.typeElem, mesh.elements)):
      nnodl = typeElem[1]
      itype = typeElem[0]

      mesh.connectivity[index:index+nnodl] = element[:nnodl]  #Asignando la conectividad
      index += nnodl
 
      mesh.offset[ielem] = index
      mesh.ctype[ielem] = vulcanType2vtk(itype)
    mesh.connectivity = mesh.connectivity[:index]
  return submeshs
