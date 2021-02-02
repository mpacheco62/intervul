#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from intervul.modpyevtk.hl import unstructuredGridToVTK
from intervul.modpyevtk.vtk import VtkMultiBlock, VtkGroup
import os

def _ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

class WriteVTK:
  def __init__(self, name,iterTime,iterSets,nsets):
    self.name = name
    self.directory = self.name + '/'
    _ensure_dir(self.directory)

    self.iterTime = iterTime
    self.iterSets = iterSets
    self.nsets = nsets
    self.timeLoop()

    groupFilesFilename = os.path.join(self.directory,self.name)
    groupFiles = VtkGroup(groupFilesFilename)
    for fileName, time in self.blockFiles:
      groupFiles.addFile(fileName,time)
    groupFiles.save()
      
  
  def def_nameResult(self):
    self.nameResult = self.name+"_"+str(self.istep)
    

  def def_setsDir(self):
    if self.nsets == 1:
      self.setsDir = self.directory
    else:
      self.setsDir = os.path.join(self.directory,self.nameResult+'/')
      _ensure_dir(self.setsDir)

  def def_multiBlockFilename(self):
    self.multiBlockFilename = os.path.join(self.directory,self.nameResult)

  def def_stepFilename(self):
      if self.nsets == 1:
        nameSet = self.nameResult
      else:
        nameSet = self.nameResult + "_" + str(self.isetIndex)
      self.stepFilename = os.path.join(self.setsDir,nameSet)


  def timeLoop(self):
    self.blockFiles = []
    for self.istep, itime in enumerate(self.iterTime()):
#      print("Step:", self.istep)
      self.def_nameResult()
      self.def_setsDir()

      self.setsLoop()
      self.def_multiBlockFilename()
      multiBlock = VtkMultiBlock(self.multiBlockFilename)
      multiBlock.addBlock(self.setsFiles)
      multiBlock.save()
      self.blockFiles.append([os.path.relpath(self.multiBlockFilename+'.vtm',self.directory),itime])

  def setsLoop(self):
    self.isetIndex = 0
    self.setsFiles = {}
    for setData in self.iterSets():
      setData = self.setsLoopWorks(setData)
      self.def_stepFilename()
      unstructuredGridToVTK(self.stepFilename,**setData)
      stepFilenameRelative = os.path.relpath(self.stepFilename,self.directory)+'.vtu'
      if setData['fieldData'] is not None and 'Set' in setData['fieldData']:
        iset = setData['fieldData']['Set']
      else:
        iset = self.isetIndex
      self.setsFiles[stepFilenameRelative] = {"index": self.isetIndex, "name": "Set "+str(iset)}
      self.isetIndex = self.isetIndex+1

     
  def setsLoopWorks(self,setData):
    return setData
    
    
