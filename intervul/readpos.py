#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from scipy.io import FortranFile
import numpy as np
from struct import *
from intervul.general import *
#from vtktools import VTK_XML_Serial_Unstructured


class VulcanPosMesh (ElemTypes):
    MECHANICAL = 1
    THERMAL = 2
    DEBUG = False
    # DEBUG = True

    def __init__(self, filename, itype, newResults=[]):
        self.mesh = Mesh()
        self.newResults = newResults
    #    print(self.newResults)
        self.filename = filename
        self.itype = itype
        self.intType = 'i4'
        self.f = FortranFile(filename)
        try:
            self.defGeneralVars()
        except ValueError:
            self.f.close()
            self.f = FortranFile(filename)
            self.intType = 'i8'
            self.defGeneralVars()
        self.readGeom()
        self.getTypeAndNnodePerElement()
    #    print("Deteccion de elementos", self.pyElemsData)

    def defGeneralVars(self):
        headerResults = []

        # ndime [0]
        headerResults.append(self.intType)

        # ndofc [1]
        headerResults.append(self.intType)

        # ndofn [2]
        headerResults.append(self.intType)

        # ngaus [3]
        headerResults.append(self.intType)

        # nhist [4]
        headerResults.append(self.intType)

        # nnode [5]
        headerResults.append(self.intType)

        # ndelem [6]
        headerResults.append(self.intType)

        # ngrup [7]
        headerResults.append(self.intType)

        # nmats [8]
        headerResults.append(self.intType)

        # npoin [9]
        headerResults.append(self.intType)

        # nprel [10]
        headerResults.append(self.intType)

        # nprop [11]
        headerResults.append(self.intType)

        # nstr1 [12]
        headerResults.append(self.intType)

        # title [13:13+8]
        headerResults.append('64<V')

        # ndata [21]
        headerResults.append(self.intType)

        # nstat [22]
        headerResults.append(self.intType)

        # ksgau [23]
        headerResults.append(self.intType)

        # nnuin [24]
        headerResults.append(self.intType)

        # nnuxx [25]
        headerResults.append(self.intType)

        # npoxx [26]
        headerResults.append(self.intType)

        # large [27]
        headerResults.append(self.intType)

        # kdyna [28]
        headerResults.append(self.intType)


        #generalVars = self.f.read_ints(np.int32)
        #print(generalVars, "len:", len(generalVars))
        generalVars = self.f.read_record(*headerResults)
        generalVars = list(generalVars) 

        #print(generalVars)
        self.ndime = generalVars.pop(0)[0]   # Numero de dimensiones
        self.ndofc = generalVars.pop(0)[0]   # Numero de grados de libertad de ¿fronteras?
        self.ndofn = generalVars.pop(0)[0]   # Numero de grados de libertad por ¿nodos?
        self.ngaus = generalVars.pop(0)[0]   # Numero de puntos de gauss
        self.nhist = generalVars.pop(0)[0]   # Numero de variables historicas
        self.nnode = generalVars.pop(0)[0]   # Numero de nodos máximos por elemnto
        self.nelem = generalVars.pop(0)[0]   # Numero de elementos de la malla
        self.ngrup = generalVars.pop(0)[0]   # Numero de sets de la malla
        self.nmats = generalVars.pop(0)[0]   # Numero de materiales de la malla
        self.npoin = generalVars.pop(0)[0]   # Numero de nodos de la malla
        self.nprel = generalVars.pop(0)[0]  # Numero de ¿propiedades de cada set?
        self.nprop = generalVars.pop(0)[0]  # Numero de ¿propiedades microestructurales? de la malla
        self.nstr1 = generalVars.pop(0)[0]  # Numero de ¿esfuerzos independientes (2d:4, 3d:6)? de la malla
        self.title = generalVars.pop(0)[0]  # El titulo del inicio del dat
        self.ndata = generalVars.pop(0)[0]  # Numero de ¿data?
        self.nstat = generalVars.pop(0)[0]  # Numero de ¿stat?
        self.ksgau = generalVars.pop(0)[0]  # No tengo idea, algo de gauss?
        self.nnuin = generalVars.pop(0)[0]  # Numero de ¿nuin?
        self.nnuxx = generalVars.pop(0)[0]  # Para mecanico = npoic, para termico =nnupc
        self.npoxx = generalVars.pop(0)[0]  # Para mecanico = 0, para termico =nporo
        self.large = generalVars.pop(0)[0]  # No se usa en mecanico, en termico deformed shape indicator
        self.kdyna = generalVars.pop(0)[0]  # Numero de ¿data?

        if self.itype == self.MECHANICAL:
            self.npoic = self.nnuxx          # ¿?
            self.nnupc = 0                   # ¿?
            self.nporo = 0                   # ¿?
            self.largex = 0                  # ¿?
            self.naccer = 1                  # ¿?
        elif self.itype == self.THERMAL:
            self.npoic = 0                   # ¿?
            self.nnupc = self.nnuxx          # ¿?
            self.nporo = self.npoxx          # ¿?
            if self.large > 0:
                self.largex = 1
            else:
                self.largex = 0
            self.naccer = 0                  # ¿?

        if self.DEBUG:
            print("ndime:", self.ndime)
            print("ndofc:", self.ndofc)
            print("ndofn:", self.ndofn)
            print("ngaus:", self.ngaus)
            print("nhist:", self.nhist)
            print("nnode:", self.nnode)
            print("nelem:", self.nelem)
            print("ngrup:", self.ngrup)
            print("nmats:", self.nmats)
            print("npoin:", self.npoin)
            print("nprel:", self.nprel)
            print("nprop:", self.nprop)
            print("nstr1:", self.nstr1)
            print("title:", self.title)
            print("ndata:", self.ndata)
            print("nstat:", self.nstat)
            print("ksgau:", self.ksgau)
            print("nnuin:", self.nnuin)
            print("nnuxx:", self.nnuxx)
            print("npoxx:", self.npoxx)
            print("large:", self.large)
            print("kdyna:", self.kdyna)
            print("npoic:", self.npoic)
            print("nnupc:", self.nnupc)
            print("nporo:", self.nporo)
            print("largex:", self.largex)
            print("naccer:", self.naccer)

    #@staticmethod
    #def __i8_to_str(i8):
    #    tostr = ""
    #    for characters in i8:
    ##      print("Hola",unpack('8s',pack('i',characters)))
    #      try:
    #          #tostr = tostr + unpack('8s',pack('i8',characters))[0].decode()
    #          tostr = "hola"
    #      except UnicodeDecodeError:
    #          pass
    #    return tostr

    def readGeom(self):
        ndime = self.ndime
        npoin = self.npoin
        npoic = self.npoic
        nnode = self.nnode
        nelem = self.nelem
        nprel = self.nprel
        ngrup = self.ngrup
        nprop = self.nprop
        nmats = self.nmats

        headerResults = []

        # nodes [0] Define las coordenadas de los nodos
        headerResults.append(_headerMat(npoin-npoic, ndime, 'f4'))

        # elements [1] Define la conectividad de los elementos  Corrige los arreglos basados en 1 y los deja basado en 0 
        headerResults.append(_headerMat(nelem, nnode, self.intType))

        # elemsSet [2] Define el set al que pertenece  Corrige los arreglos basados en 1 y los deja basado en 0 
        headerResults.append(_headerVec(nelem, self.intType))

        # proel [3] Define propiedades para cada set
        headerResults.append(_headerMat(ngrup, nprel, 'f4'))

        # props [4] Propiedades ¿micro?
        headerResults.append(_headerMat(nmats, nprop, 'f4'))

        # null [5]
        headerResults.append(_headerVec(11, self.intType))

        # istat [6] otro puntero
        headerResults.append(_headerVec(8, self.intType))

        geom = self.f.read_record(*headerResults)

        # nodes
        self.mesh.nodes = geom[0]

        # lnods
        self.mesh.elements = geom[1] - 1

        # matno
        self.mesh.elemsSet = geom[2] - 1

        # proel
        self.proel = geom[3]

        # props
        self.mesh.props = geom[4]

        # istat
        self.mesh.istat = geom[6]

        self.mesh.createiFile()

        if self.DEBUG:
            print("Nodes: ", self.mesh.nodes)
            print("Elements: ", self.mesh.elements)
            print("ElemsSet: ", self.mesh.elemsSet)


    def __iter__(self):
        filename = self.filename
        itype = self.itype
        if self.f:
            self.f.close()
        self.__init__(filename, itype, newResults=self.newResults)
        return self

    def __next__(self):
        output = self.readResult()
        if output is False:
            raise StopIteration
        return output['istep'], output
    next = __next__  # Compatibilidad entre python 2 y 3


    def readResult(self):
        result = Results(self.newResults)
        result['Vulcan_ipoin'] = self.mesh.inodeFile
        result['Vulcan_ielem'] = self.mesh.ielemFile
        THERMAL = self.THERMAL
        MECHANICAL = self.MECHANICAL
        itype = self.itype
        ndofc = self.ndofc
        npoin = self.npoin
        npoic = self.npoic
        kdyna = self.kdyna
        ksgau = self.ksgau
        nnuin = self.nnuin
        nstr1 = self.nstr1
        ndime = self.ndime
        nnupc = self.nnupc
        large = self.large
        nporo = self.nporo

        headerResults = []

        # titleResult [0]
        headerResults.append('64<V')

        # subtitle [1]
        headerResults.append('64<V')

        # itime [2]
        headerResults.append(self.intType)

        # istep [3]
        headerResults.append(self.intType)

        # iiter [4]
        headerResults.append(self.intType)

        # TimeValue [5]
        headerResults.append('f4')

        # displacement or temperature [6] (disto)
        headerResults.append(_headerMat(npoin-npoic, ndofc))

        try:
            resultData = self.f.read_record(*headerResults)
        except:
            return False

        result['titleResult'] = unpack('64s',resultData[0])[0]
        result['itime'] = resultData[2][0]
        result['istep'] = resultData[3][0]
        result['iiter'] = resultData[4][0]
        result['TimeValue'] = resultData[5][0]
        if self.itype == MECHANICAL:
            result['displacement'] = resultData[6]
        else:
            result['temperature'] = resultData[6]

        if self.DEBUG:
            print("titleRes:", result['titleResult'])
            # print("subtitle:", result['subtitle'])
            print("itime:", result['itime'])
            print("istep:", result['istep'])
            print("iiter:", result['iiter'])
            print("ttime:", result['TimeValue'])
            if itype == MECHANICAL:
                print("displac:", result['displacement'])
            else:
                print("Temperature:", result['temperature'])

        self.velocityExist = False
        self.accelerationExist = False
        self.reactionExist = False
        self.stressExist = False
        self.strainExist = False
        self.tempRateExist = False
        self.thermalDisplacExist = False
        self.phaseChangeExist = False
        self.fluxExist = False
        self.internalExist = False
        self.porosityExist = False

        if itype == MECHANICAL:
            if kdyna > 0:                            # velocities & accelerations (only mechanical for dynamic problems)
                self.velocityExist = True
                self.accelerationExist = True
            self.reactionExist = True                # reactions (only mechanical; itype=1)
            if ksgau != 0:                           # internal variables (mechanical or thermal)
                self.stressExist = True
                self.strainExist = True
                if nnuin != 0:
                    self.internalExist = True

        if itype == THERMAL:
            if kdyna > 0:                            # temperature rates (only thermal for transient problems)
                self.tempRateExist = True
            if large > 0:                            # displacements (only thermal for large strain problems)
                self.thermalDisplacExist = True
            if nnupc > 0:                             # phase-change function (only thermal; itype=2)
                self.phaseChangeExist = True
            if ksgau != 0:
                if self.istat[2] != self.istat[3]:     # internal variables (mechanical or thermal)
                    self.fluxExist = True
                if nnuin != 0:                         # internal variables (mechanical or thermal)
                    self.internalExist = True
                if nporo != 0:                         # porosity criteria (only thermal; itype=2)
                    self.porosityExist = True
        if self.DEBUG:
            print("TO REEEEEAAAAAADDDDD**************")
            if self.velocityExist: print("Velocity")
            if self.accelerationExist: print("Acceleration")
            if self.tempRateExist: print("Temperature Rates")
            if self.thermalDisplacExist: print("Thermal Displac")
            if self.reactionExist: print("Reactions")
            if self.phaseChangeExist: print("Phase Change")
            if self.stressExist: print("Stress")
            if self.strainExist: print("Strain")
            if self.fluxExist: print("Flux")
            if self.internalExist: print("Internal")
            if self.porosityExist: print("Porosity")

        if self.velocityExist and self.accelerationExist:
            headerResults = _headerMat(npoin-npoic, ndofc)
            temp = self.f.read_record(headerResults, headerResults)
            result['velocity']     = temp[0]
            result['acceleration'] = temp[1]

        if self.tempRateExist:
            result['tempRate'] = _readMat(self.f, npoin-npoic, ndofc)
        if self.thermalDisplacExist:
            result['displacement'] = _readMat(self.f, npoin, ndime)
        if self.reactionExist:
            result['reaction'] = _readMat(self.f, npoin, ndofc)
        if self.phaseChangeExist:
            result['phaseChange'] = _readMat(self.f, npoin, nnupc)

        if self.stressExist and self.strainExist:
            headerResults = []
            headerResults.append(_headerMat(npoin-npoic, nstr1))
            headerResults.append(_headerMat(npoin-npoic, nstr1))
            if self.internalExist:
                headerResults.append(_headerMat(npoin-npoic, nnuin))
            temp = self.f.read_record(*headerResults)

            result['stress'] = temp[0]
            result['strain'] = temp[1]
            if self.internalExist:
                result['internal'] = temp[2]

        if self.fluxExist:
            result['flux'] = _readMat(self.f, npoin-npoic, nstr1)
        if itype == THERMAL and self.internalExist:
            result['internal'] = _readMat(self.f, npoin-npoic, nnuin)
        if self.porosityExist:
            result['porosity'] = _readMat(self.f, npoin, nporo)

        result.updateNewResults()
        return result

    def getTypeAndNnodePerElement(self):
      self.mesh.typeElem=np.empty((self.nelem,2),dtype=int)
      for ielem,elem in enumerate(self.mesh.elements):
        #lgrup = self.matno[ielem]    # El set al que pertence
        lgrup = self.mesh.elemsSet[ielem]    # El set al que pertence
        nnodl = self.proel[lgrup,2-1]   # Los arreglos parten de 0 y es el numero de nodos que tiene el elemento
        ltype = self.proel[lgrup,5-1]   # Los arreglos parten de 0 y es el tipo de elemento, 30,32, etc
        ntype = self.proel[lgrup,6-1]   # Los arreglos parten de 0 y que tipo de elemento es, axisimetrico, linea, 3d, etc
        if self.getElemType(nnodl,ntype):
          pyTypeElem = self.getElemType(nnodl,ntype)
        else:
          raise TypeError("no se encontró el elemento para nnodl: ",nnodl,ntype)
        self.mesh.typeElem[ielem,0] = pyTypeElem
        self.mesh.typeElem[ielem,1] = nnodl


def _headerMat(idime, jdime, itype='f4'):
    return '(' + str(idime) + ',' + str(jdime) + ')<'+itype


def _headerVec(idime, itype='f4'):
    return str(idime) + '<'+itype


def _readMat(fortranFile, idime, jdime, itype='f4'):
    return fortranFile.read_record(_headerMat(idime, jdime, itype))
