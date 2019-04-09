"""Imports geometry from Rhino files into grasshopper.
   Preserves layer hierarchy as data tree.
    Inputs:
        filename: List of file(s) to import (string)
        Import: boolean to start import
        deleteExisting: boolean to delete existing geometry in file
    Output:
        geometryOut: The imported geometry ingo gh space."""

__author__ = "jberry"
__version__ = "2019.03.11"

ghenv.Component.Name = "Batch Import"
ghenv.Component.NickName = "BatchImport"

import rhinoscriptsyntax as rs
import scriptcontext as sc
import ghpythonlib.treehelpers as th
import Rhino
import os
rcdoc = Rhino.RhinoDoc.ActiveDoc


"""
Deletes existing geometry from Rhino file before import.
"""
def deleteExistingGeom():
    sc.doc = Rhino.RhinoDoc.ActiveDoc
    objects = rs.AllObjects()
    for obj in objects:
        rs.DeleteObject(obj)
    return

"""
Imports geometry from files

"""
def importRhinoFile(fileNames, sourcePath):
    #file import
    for fn in fileNames:
        thisFilePath = os.path.join(sourcePath,fn)
        importCommandString = '_-Import "' + thisFilePath + '" _Enter'
        imported = rs.Command(importCommandString, echo=False)
            
        if not imported:
            print "there was a problem with file: " + fn
        
    return
    

"""
Grabs geometry from Rhino and constructs data tree.
Each branch of the tree is a different layer in the document.
"""
def rhinoGeomToDataTree():
    sc.doc = rcdoc
    layers = rs.LayerNames(sort=False)
    sc.doc = ghdoc
#    print layers
    layerTree = [[] for layer in layers]
    for i in range(len(layers)):
        objs = Rhino.RhinoDoc.ActiveDoc.Objects.FindByLayer(layers[i])
#        print(objs)
        
        if objs:
            geoms = [obj.Geometry for obj in objs]
            layerTree[i].extend(geoms)
#    print(layerTree)
    
    layerTree = th.list_to_tree(layerTree, source=[])
    
    return layerTree


#Perform Import
if Import:
    # option to delete existing geometry in document
    if deleteExisting:
        deleteExistingGeom()
        
    #now import geometry from files
    if (filenames != None) and (sourceFolderPath != None):
        #import function here
        importRhinoFile(filenames, sourceFolderPath)
        geometryOut=rhinoGeomToDataTree() #output geometry to gh here
    else:
        if filenames==None:
            print "Provide a list of filenames"
        elif sourceFolderPath==None:
            print "Provide the path to your source folder"
#        elif len(layers)<=0:
#            print "Please specify which layers you would like to import."
        else:
            print "Something went wrong... please check all input types."
    