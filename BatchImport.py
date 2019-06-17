"""Imports geometry from Rhino files into grasshopper.
   Preserves layer hierarchy as data tree.
    Inputs:
        filename: List of file(s) to import (string)
        Import: boolean to start import
        deleteExisting: boolean to delete existing geometry in file
    Output:
        geometryOut: The imported geometry ingo gh space."""

__author__ = "jberry"
__version__ = "2019.05.24"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import ghpythonlib.treehelpers as th
import os
rcdoc = Rhino.RhinoDoc.ActiveDoc
ghdoc = sc.doc

class MyComponent(component):
    """
    Deletes existing geometry from Rhino file before import.
    """
    def deleteExistingGeom(self):
        sc.doc = Rhino.RhinoDoc.ActiveDoc
        objects = rs.AllObjects()
        if objects:
            for obj in objects:
                rs.DeleteObject(obj)
        layers = rs.LayerNames()
        for layer in layers:
            if layer!=rs.CurrentLayer():
                rs.DeleteLayer(layer)
        return
    
    """
    Imports geometry from files
    
    """
    def importRhinoFile(self, fileNames, sourcePath):
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
    def rhinoGeomToDataTree(self):
        sc.doc = rcdoc
        layers = rs.LayerNames(sort=False)
        sc.doc = ghdoc
    #    layerTree = [[] for layer in layers]
        layerTree = []
        for i in range(len(layers)):
            objs = Rhino.RhinoDoc.ActiveDoc.Objects.FindByLayer(layers[i])
            
            if objs:
                geoms = [obj.Geometry for obj in objs]
    #            layerTree[i].extend(geoms)
                layerTree.append(geoms)
        status= str(len(layerTree))+ " branches \n"
        
        layerTree = th.list_to_tree(layerTree, source=[])
        
        return layerTree, status
    
    def RunScript(self, filenames, sourceFolderPath, Import, deleteExisting):
        geometryOut, status = None, None
        
        #Perform Import
        if Import:
            # option to delete existing geometry in document
            status = "start import \n"
            if deleteExisting:
                self.deleteExistingGeom()
                status += "deleted \n"
                
            #now import geometry from files
            if (filenames != None) and (sourceFolderPath != None):
                #import function here
                self.importRhinoFile(filenames, sourceFolderPath)
                status += "imported rhino files \n"
#                thisDoc.ScheduleSolution(20, self.rhinoGeomToDataTree)
                geometryAndStatus=self.rhinoGeomToDataTree()
                geometryOut = geometryAndStatus[0]
                status+=geometryAndStatus[1]
                status += "geometry to datatree \n"
            else:
                if filenames==None:
                    print "Provide a list of filenames"
                elif sourceFolderPath==None:
                    print "Provide the path to your source folder"
        
        # return outputs if you have them; here I try it for you:
        return (geometryOut, status)
