"""Imports geometry from Rhino files into grasshopper. Preserves layer hierarchy as data tree.
    Inputs:
        filename: List of file(s) to import (string)
        Import: boolean to start import
        deleteExisting: boolean to delete existing geometry in file
    Output:
        geometryOut: The imported geometry into gh space.
		
	WARNING:
		Still buggy. Throw (component) has expired error for some reason.
		Import still works, so I'm not sure why that error is happening."""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino, os
import rhinoscriptsyntax as rs
import scriptcontext as sc
import ghpythonlib.treehelpers as th

rcdoc = Rhino.RhinoDoc.ActiveDoc
ghdoc = sc.doc

__author__ = "jberry"
__version__ = "2019.05.02"

class MyComponent(component):
    
    """
    ERROR WHEN DELETING ALL OBJECTS!!!!!
    Deletes existing geometry from Rhino file before import.
    """
    def deleteExistingGeom(self):
        sc.doc = rcdoc
        objects = rs.AllObjects()
        for obj in objects:
            rs.DeleteObject(obj)
        sc.doc=ghdoc
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
        layerTree = [[] for layer in layers]
        for i in range(len(layers)):
            objs = Rhino.RhinoDoc.ActiveDoc.Objects.FindByLayer(layers[i])
            if objs:
                geoms = [obj.Geometry for obj in objs]
                layerTree[i].extend(geoms)
        layerTree = th.list_to_tree(layerTree, source=[])
        return layerTree
    
    """
    To run the script and import files
    """
    def RunScript(self, filenames, sourceFolderPath, Import, deleteExisting):
        self.Name = "Batch Import"
        self.NickName = "BatchImport"
        geometryOut = None
        
        if Import:
            # option to delete existing geometry in document
            if deleteExisting:
                self.deleteExistingGeom()
                
            #now import geometry from files
            if (filenames != None) and (sourceFolderPath != None):
                #import function here
                self.importRhinoFile(filenames, sourceFolderPath)
                geometryOut=self.rhinoGeomToDataTree() #output geometry to gh here
            else:
                if filenames==None:
                    print "Provide a list of filenames"
                elif sourceFolderPath==None:
                    print "Provide the path to your source folder"
                else:
                    print "Something went wrong... please check all input types."
        return geometryOut
