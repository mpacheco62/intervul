#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Modulo con clases generales

Es un modulo de clases generales, para almacenar información y trabajar con
ella. Las cuales pueden ser:

- Mesh: un contendor de mallas
- Results: un contenedor de resultados de vulcan
- AddResults: una clase especial que sirve para agregar resultados a la clase
  anterior


"""

from __future__ import unicode_literals
from __future__ import print_function
import numpy as np
# from struct import *
# from vtktools import VTK_XML_Serial_Unstructured


class ElemTypes(object):
    """Clase Element Types (ElemTypes) o de tipos de elementos.

    Su funcion es ser una clase estatica que define valores comunes.

    Attributes
    ----------
    HEXA8 : `ElemTypes.HEXA8`
        Representa el elemento Hexaedrico de 8 nodos para vulcan.
    HEXA20 : `ElemTypes.HEXA20`
        Representa el elemento Hexaedrico de 20 nodos para vulcan.
    TETR4 : `ElemTypes.TETR4`
        Representa el elemento Tetraedrico de 4 nodos para vulcan.
    TETR10 : `ElemTypes.TETR10`
        Representa el elemento Tetraedrico de 10 nodos para vulcan.
    TOBL6 : `ElemTypes.TOBL6`
        Representa el elemento Tobleron de 6 nodos para vulcan.
    TRIA3 : `ElemTypes.TRIA3`
        Representa el elemento Triangular de 3 nodos para vulcan.
    TRIA6 : `ElemTypes.TRIA6`
        Representa el elemento Triangular de 6 nodos para vulcan.
    QUAD4 : `ElemTypes.QUAD4`
        Representa el elemento Cuadrilatero de 4 nodos para vulcan.
    QUAD8 : `ElemTypes.QUAD8`
        Representa el elemento Cuadrilatero de 8 nodos para vulcan.
    LINE2 : `ElemTypes.LINE2`
        Representa el elemento Lineal de 2 nodos para vulcan.

    Examples
    --------
    >>> from intervul.general import ElemTypes
    >>> ElemTypes.getElemType(nnodl = 8, ntype = 4)
    1
  """
    HEXA8 = 1
    HEXA20 = 2
    TETR4 = 3
    TETR10 = 4
    TOBL6 = 5
    TRIA3 = 6
    TRIA6 = 7
    QUAD4 = 8
    QUAD8 = 9
    LINE2 = 10
    elemInfo = {
        HEXA8: {
            'nnodl': 8,
            'ntype': [4]
        },
        HEXA20: {
            'nnodl': 20,
            'ntype': [4]
        },
        TETR4: {
            'nnodl': 4,
            'ntype': [4]
        },
        TETR10: {
            'nnodl': 10,
            'ntype': [4]
        },
        TOBL6: {
            'nnodl': 6,
            'ntype': [4]
        },
        TRIA3: {
            'nnodl': 3,
            'ntype': [1, 2, 3]
        },
        TRIA6: {
            'nnodl': 6,
            'ntype': [1, 2, 3]
        },
        QUAD4: {
            'nnodl': 4,
            'ntype': [1, 2, 3]
        },
        QUAD8: {
            'nnodl': 8,
            'ntype': [1, 2, 3]
        },
        LINE2: {
            'nnodl': 2,
            'ntype': [1, 2, 3, 5]
        },
    }

    @staticmethod
    def getElemType(nnodl, ntype):
        """ Obtiene el tipo de elemento según parámetros de Vulcan

        Método que devuelve el tipo de elemento de vulcan para usarlo con
        otras funciones o clases.

        Parameters
        ----------
        nnodl: int
            Número de nodos del elemento.
        ntype: int
            Número del tipo de elemento (tensión plana, def plana,
            axisimétrico, etc..) de Vulcan (ntype del set).

        Returns
        -------
        int
            El número del tipo de elemento que corresponde (HEX8, HEX20, QUAD8,
            etc...)

        """
        for elemType, data in ElemTypes.elemInfo.items():
            if data['nnodl'] == nnodl and ntype in data['ntype']:
                return elemType
        return False


class BaseMesh(ElemTypes):
    """Clase BaseMesh (malla base) que es la unidad básica de malla

    La clase malla base, representa de manera general una malla para utilizarla
    en distintos objetos. El orden de las matrices es del estilo "C" y basado
    en cero. Además, el arreglo de los elementos debe estar basado en cero,
    esto es que el siguiente elemento es valido ``[0, 1, 2, 3]``.

    Attributes
    ----------
    nodes : array_like
        Es una matriz de nodos (cantidad de nodos, dimensión).
    elements : array_like
        Es una matriz que contiene todos los elementos de la malla este tiene
        la estructura (cantidad de elementos, máxima cantidad de nodos por
        elementos).
    typeElem : array_like
        Es una matriz de (cantidad de elementos, 2), la primera columna
        representa el tipo de elemento que es de acuerdo a ``ElemTypes`` y la
        segunda, la cantidad de nodos que tiene ese elemento.
    elemsSet : array_like
        Es una matriz que indica a que Set pertenece cada elementos.
    nodeUniqueTemp: set
        Es un set temporal para saber que cuales son los nodos que contiene la
        submalla.
    ielemFile: array_like
        Es una matriz que relaciona el elemento actual y el elemento que
        corresponde en el archivo original de datos.
    inodeFile: array_like
        Es una matriz que relaciona el nodo actual y el nodo que corresponde en
        el archivo original de datos.
    """
    def __init__(self):
        self.nodes = []
        self.elements = []
        self.typeElem = []  # [ElemType,nnodl]
        self.elemsSet = []
        self.ielemFile = []
        self.inodeFile = []

    def createiFile(self):
        """ Crea internamente un puntero a los nodos y elementos originales del
        archivo.

        Función que crea los arreglos ``self.inodeFile`` y ``self.ielemFile``,
        estos contienen la numeración de los archivos originales de los nodos y
        elementos de la malla.

        """
        self.inodeFile = np.arange(1, self.nodes.shape[0] + 1)
        self.ielemFile = np.arange(1, self.elements.shape[0] + 1)

    def getElemsOriginal(self):
        """ Devuelve un arreglo con los elementos en el estado del archivo.

        Función que cambia el nodo de cada elemento de acuerdo al orden del
        archivo original ``self.ielemFile``.
        """
        elems = np.zeros(self.elements.shape, dtype=int)
        for ielem, [element, nnodes] in enumerate(zip(self.elements, self.typeElem[:, 1])):
            elems[ielem, :nnodes] = [self.inodeFile[inode] for inode in element[:nnodes]]
        return elems

    def nodes3d(self):
        """ Convierte la malla 2D a una 3D

        Función que transforma la malla 2D a una 3D agregando la columna "z" y
        rellenando con ``0`` al arreglo de nodos ´´self.nodes``

        Returns
        -------
        array_like
            Retorna los el nuevo arreglo de nodos ``self.nodes``
        """
        ndim = self.nodes.shape[1]
        ndata = self.nodes.shape[0]
        if ndim == 2:
            self.nodes = np.hstack(
                (self.nodes, np.full((ndata, 1), 0, dtype=self.nodes.dtype)))
            return self.nodes
        else:
            return self.nodes

    def splitCoordinates(self):
        """ Separa las nodos por coordenadas

        Función que separa internamente la matriz de nodos numpy
        ``[[x0,y0,z0][x1,y1,z1][...,...,...]]``` en 3 arreglos columnas
        distintos ``self.x``, ``self.y`` y ``self.z``

        Returns
        -------
        list
            Retorna los tres vectores de nodos ``[x, y, z]``
        """
        ndim = self.nodes.shape[1]
        self.x = self.nodes[:, 0].copy()
        self.y = self.nodes[:, 1].copy()
        if ndim == 3:
            self.z = self.nodes[:, 2].copy()
        return self.x, self.y, self.z

    @staticmethod
    def _invertList(toInvert, indexStart=0):
        tempInvert = {}
        for i, value in enumerate(toInvert, indexStart):
            tempInvert[value] = i
        return tempInvert

    def nnodes(self):
        """ Entrega el número de nodos de la malla

        Returns
        -------
        int
            Retorna el número de nodos de la malla
        """
        return self.nodes.shape[0]

    def nelems(self):
        """ Entrega el número de elementos de la malla

        Returns
        -------
        int
            Retorna el número de elementos de la malla
        """
        return self.elements.shape[0]

    def _listToNumpy(self):
        self.nodes = np.array(self.nodes, dtype=float)
        self.inodeFile = np.array(self.inodeFile, dtype=float)
        self.elements = np.array(self.elements, dtype=int)
        self.ielemFile = np.array(self.ielemFile, dtype=int)
        self.typeElem = np.array(self.typeElem, dtype=int)


class Submesh(BaseMesh):
    """Clase Submesh, que define mallas pequeñas de otras

    La clase Submesh permite trabajar con submallas obtenidas de otra malla,
    el cambio principal radica en que se agregan los atributos
    ``ielemOriginal``, ``inodeOriginal`` y se cambia el uso de ``elemsSet``
    que deja de ser un arreglo y pasa a ser solo un número.

    Otro aspecto importante es que la numeración de los nodos cambia,
    permitiendo que se utilice como una malla totalmente independiente y con
    todos los nodos y elementos partiendo de 0.

    Attributes
    ----------
    ielemOriginal : array_like
        Es un vector que indica la posición original de cada elemento respecto
        del original.
    inodeOriginal : array_like
        Es un vector que indica la posición original de cada nodo respecto del
        original.
    elemsSet: int
        Define a que set pertenece esta malla
    """
    # TODO Definir que se usa para el elemsset base 0 o base 1
    def __init__(self, setNum=None):
        super(Submesh, self).__init__()
        self._nodeUniqueTemp = set()
        self.ielemOriginal = []
        self.inodeOriginal = []
        self.elemsSet = setNum

    def _listToNumpy(self):
        super(Submesh, self)._listToNumpy()
        self.ielemOriginal = np.array(self.ielemOriginal, dtype=int)
        self.inodeOriginal = np.array(self.inodeOriginal, dtype=int)

    def _updateByNodeUniqueTemp(self, mesh):
        self.inodeOriginal = np.array(sorted(self._nodeUniqueTemp))

        for inode in self.inodeOriginal:
            self.nodes.append(mesh.nodes[inode, :])
            self.inodeFile.append(mesh.inodeFile[inode])

        tempInvertNode = mesh._invertList(self.inodeOriginal,
                                          indexStart=0)
        for ielem, elem in enumerate(self.elements):
            tempElem = [tempInvertNode[inode] for inode in elem]
            self.elements[ielem] = tempElem
            self.ielemFile.append(mesh.ielemFile[ielem])

        self._listToNumpy()

    def getSet(self, mesh):
        """ Transforma esta submalla a un set de la malla principal ``mesh``

        Función que extrae toda la información de un set de la malla ``mesh``
        y crea una nueva malla en base a este set, los nodos de esta malla
        nueva parten de 0 y los nodos en los elementos también están
        renumerados para concordar y ser una malla independiente de la
        original. Los punteros ``self.ielemOriginal`` y ``self.inodeOriginal``
        relacionan los nodos de esta malla con la de su padre
        """
        if not (self.elemsSet in mesh.elemsSet):
            raise("No existe el set en la malla")

        for ielem, (itype, elemSet, tempElem) in enumerate(
                zip(mesh.typeElem, mesh.elemsSet, mesh.elements)):
            if self.elemsSet == elemSet:
                nnodl = itype[1]
                elem = tempElem[:nnodl]
                self._nodeUniqueTemp.update(elem)
                self.elements.append(elem)
                self.typeElem.append(itype)
                self.ielemOriginal.append(ielem)

        self._updateByNodeUniqueTemp(mesh)


class Mesh(BaseMesh):
    """Clase Mesh (Malla) que representa una malla.

    La clase malla es un manejador de la clase ``BaseMesh`` que agrega la
    funcionalidad de poder separar las mallas de acuerdo a sets, estas
    submallas son objetos de la clase ``Submesh``.

    Examples
    --------
    >>> from intervul.general import Mesh
    >>> ElemTypes.getElemType(nnodl = 8, ntype = 4)
    1
  """
    def __init__(self):
        super(Mesh, self).__init__()
        self.splitted = False

    def splitMeshBySet(self):
        meshSets = np.unique(self.elemsSet)
        # Crea mallas para cada set
        splitted = {}
        for iset in meshSets:
            # Por el cambio de 1 based a 0
            splitted[iset] = Submesh(setNum=iset + 1)

        for ielem, (itype, elemSet, tempElem) in enumerate(
                zip(self.typeElem, self.elemsSet, self.elements)):
            nnodl = itype[1]
            elem = tempElem[:nnodl]
            splitted[elemSet]._nodeUniqueTemp.update(elem)
            splitted[elemSet].elements.append(elem)
            splitted[elemSet].typeElem.append(itype)
            splitted[elemSet].ielemOriginal.append(ielem)


        for elemSet, submesh in splitted.items():
            submesh._updateByNodeUniqueTemp(self)
        self.submeshs = splitted
        return splitted


class AddResults:
    def __init__(self, dim, itype, name, fun):
        self.dim = dim
        self.itype = itype
        self.name = name
        self.fun = fun


class Results:
    NODAL = 1
    CELL = 2
    FIELD = 3

    def addNewResults(self):
        for newResult in self.newResults:
            arrItype, arrDim, arrName = np.atleast_1d(newResult.itype,
                                                      newResult.dim,
                                                      newResult.name)
            for itype, dim, name in zip(arrItype, arrDim, arrName):
                if dim != 'scalars' and dim != 'vectors' and dim != 'tensors':
                    raise TypeError(
                        "La dimension solo puede ser scalars vectors tensors")
                if itype == 'nodal':
                    self.nodal[dim][name] = None
                    self.inverse[name] = [self.NODAL, dim]
                elif itype == 'cell':
                    self.cell[dim][name] = None
                    self.inverse[name] = [self.CELL, dim]
                elif itype == 'field':
                    self.field[dim][name] = None
                    self.inverse[name] = [self.FIELD, None]
                else:
                    raise TypeError(
                        "Se ingreso mal el tipo, solo pueden ser nodal cell o "
                        "field"
                    )

    def updateNewResults(self):
        for newResult in self.newResults:
            arrName = np.atleast_1d(newResult.name)
            results = newResult.fun(self)
            if type(results) is not list:
                results = [results]
            for name, result in zip(arrName, results):
                self[name] = result

    def __init__(self, newResults=[]):
        self.newResults = newResults
        self.nodal = {
            'scalars': {
                'tempRate': None,
                'phaseChange': None,
                'internal': None,
                'porosity': None,
                'Vulcan_ipoin': None,
            },
            'vectors': {
                'displacement': None,
                'velocity': None,
                'acceleration': None,
                'reaction': None,
                'thermalDisplac': None,
            },
            'tensors': {
                'stress': None,
                'strain': None,
                'flux': None,
            }
        }
        self.cell = {
            'scalars': {
                'Vulcan_ielem': None
            },
            'vectors': {},
            'tensors': {}
        }
        self.field = {
            'titleResult': None,
            'subtitle': None,
            'itime': None,
            'istep': None,
            'iiter': None,
            'TimeValue': None
        }
        self.inverse = {
            'tempRate': [self.NODAL, 'scalars'],
            'phaseChange': [self.NODAL, 'scalars'],
            'internal': [self.NODAL, 'scalars'],
            'porosity': [self.NODAL, 'scalars'],
            'Vulcan_ipoin': [self.NODAL, 'scalars'],
            'displacement': [self.NODAL, 'vectors'],
            'velocity': [self.NODAL, 'vectors'],
            'acceleration': [self.NODAL, 'vectors'],
            'reaction': [self.NODAL, 'vectors'],
            'thermalDisplac': [self.NODAL, 'vectors'],
            'stress': [self.NODAL, 'tensors'],
            'strain': [self.NODAL, 'tensors'],
            'flux': [self.NODAL, 'tensors'],
            'Vulcan_ielem': [self.CELL, 'scalars'],
            'titleResult': [self.FIELD, None],
            'subtitle': [self.FIELD, None],
            'itime': [self.FIELD, None],
            'istep': [self.FIELD, None],
            'iiter': [self.FIELD, None],
            'TimeValue': [self.FIELD, None]
        }
        self.addNewResults()

    def __setitem__(self, index, value):
        itype, dim = self.inverse[index]
        if itype is self.FIELD:
            self.field[index] = value
        elif itype is self.NODAL:
            self.nodal[dim][index] = value
        elif itype is self.CELL:
            self.cell[dim][index] = value

        if index == 'Vulcan_ielem':
            self.inverseVulcan_ielem = dict()
            for ilocalElem, ivulcanElem in enumerate(
                            self.cell['scalars']['Vulcan_ielem']):
                self.inverseVulcan_ielem[ivulcanElem] = ilocalElem

    def getlocalielem(self, ivulcanElem):
        return self.inverseVulcan_ielem[ivulcanElem]

    def __getitem__(self, index):
        itype, dim = self.inverse[index]
        if itype is self.FIELD:
            return self.field[index]
        elif itype is self.NODAL:
            return self.nodal[dim][index]
        elif itype is self.CELL:
            return self.cell[dim][index]

    def getResults(self, transformTo3D=False, which="all"):

        t3d = transformTo3D
        nodalResults = False
        cellResults = False
        fieldResults = False
        if which == "all":
            nodalResults = True
            cellResults = True
        elif which == "nodal":
            nodalResults = True
        elif which == "cell":
            cellResults = True
        elif which == "field":
            fieldResults = True
        else:
            raise TypeError("No se reconoce que resultados")

        allRes = {}
        if fieldResults:
            for name, data in self.field.items():
                if data is not None:
                    allRes[name] = data

        if nodalResults:
            for name, data in self.nodal['scalars'].items():
                if data is not None:
                    allRes[name] = data

            for name, data in self.nodal['vectors'].items():
                if data is not None:
                    allRes[name] = self._vecTo(data, t3d)

            for name, data in self.nodal['tensors'].items():
                if data is not None:
                    allRes[name] = self._tenTo(data, t3d)

        if cellResults:
            for name, data in self.cell['scalars'].items():
                if data is not None:
                    allRes[name] = data

            for name, data in self.cell['vectors'].items():
                if data is not None:
                    allRes[name] = self._vecTo(data, t3d)

            for name, data in self.cell['tensors'].items():
                if data is not None:
                    allRes[name] = self._tenTo(data, t3d)

        return allRes

    @staticmethod
    def _vecTo(data, transform=True):
        ndim = data.shape[1]
        ndata = data.shape[0]
        if ndim == 2 and transform:
            empty = np.full((ndata, 1), 0, dtype=data.dtype)
            return np.hstack((data, empty))
        else:
            return data

    @staticmethod
    def _tenTo(data, transform=True):
        ndim = data.shape[1]
        ndata = data.shape[0]
        if ndim == 4 and transform:
            # viene como:   x  y xy z
            # llegar a  :   x  y  z xy yz xz
            empty = np.full((ndata, 1), 0, dtype=data.dtype)
            #                      x            y            z
            #                      xy        yz     xz
            return np.hstack((data[:, 0:1], data[:, 1:2], data[:, 3:4],
                              data[:, 2:3], empty, empty))
        elif ndim == 6:
            #                        x            y            z
            #                        xy           yz           xz
            return np.hstack((data[:, 0:1], data[:, 1:2], data[:, 3:4],
                              data[:, 2:3], data[:, 5:6], data[:, 4:5]))
        else:
            return data
#                                                               ! 1-> y;
#                                                               ! 2-> xy;
#                                                               ! 3-> z;
#                                                               ! 4-> xz
#                                                               ! 5-> yz;

    def updateBySplitMesh(self, mesh, results=['all']):
        newResults = Results(self.newResults)

        if results[0] == 'all':
            for name, data in self.field.items():
                newResults.field[name] = data

            # for inewnode, ioldnode in enumerate(mesh.inodeOriginal):
            for itype, results in self.nodal.items():
                for name, data in results.items():
                    newResults.nodal[itype][name] = self._subNP(data,
                                                          (mesh.inodeOriginal, slice(None)))

            # for inewelem, ioldelem in enumerate(mesh.ielemOriginal):
            for itype, results in self.cell.items():
                for name, data in results.items():
                    newResults.cell[itype][name] = self._subNP(data,
                                                               (mesh.ielemOriginal, slice(None)))
        else:
            for name in results:
                jtype, itype = self.inverse[name]
                if jtype == self.NODAL:
                    newResults[name] = self._subNP(self[name],
                                                   (mesh.inodeOriginal, slice(None)))
                elif jtype == self.CELL:
                    newResults[name] = self._subNP(self[name],
                                                   (mesh.ielemOriginal, slice(None)))
                elif jtype == self.FIELD:
                    newResults[name] =  self[name]

        newResults.field['Set'] = mesh.elemsSet
        newResults.inverse['Set'] = [self.FIELD, None]
        return newResults

    @staticmethod
    def _emptyArray(ndata, data):
        if data is not None:
            if data.ndim == 1:
                return np.empty((ndata), dtype=data.dtype)
            else:
                return np.empty((ndata, data.shape[1]), dtype=data.dtype)
        else:
            return None

    @staticmethod
    def _subNP(data, indData):
        if data is not None:
            if data.ndim == 1:
                return data[indData[0]]
            else:
                return data[indData[0], indData[1]]
        else:
            return None

    @staticmethod
    def _assignNpToNp(toSave, indToSave, data, indData):
        if data is not None:
            if indToSave[1] == slice(None) and indData[1] == slice(
                    None) and data.ndim == 1:
                toSave[indToSave[0]] = data[indData[0]]
            else:
                toSave[indToSave[0], indToSave[1]] = data[indData[0],
                                                          indData[1]]
        else:
            return None
