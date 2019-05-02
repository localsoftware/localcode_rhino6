"""Exports geometry to a new file.
    Inputs:
        geometry: Data tree of geometry. Each branch corresponds to a layer.
        exportFileName: Export file name.
        exportFilePath: Target directory.
        layerNames: List of layer names to bake geometry into. 
        layerColors: List of colors (Optional). Can be one color or
                     as many colors as layer names. 
        Export: boolean to run component
        deleteExisting: boolean to delete geometry already in document.
    Output:
        status: status of export
		
	WARNING:
		Still buggy. Sometimes has trouble baking objects into Rhino document.
		Also sometimes throws error deleting objects.
		Sometimes throws error when creating new layers."""
                
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino, os
import rhinoscriptsyntax as rs
import scriptcontext as sc
import ghpythonlib.treehelpers as th
import ghpythonlib.components as ghcomp

rcdoc = Rhino.RhinoDoc.ActiveDoc
ghdoc = sc.doc

__author__ = "jberry"
__version__ = "2019.05.02"

class MyComponent(component):
    
    """
    Bake objects into rhino file
    """
    def bake(self, geometry, layerNames, layerColors):
        geometryList = [geometry.Branch(b) for b in range(geometry.BranchCount)]
        if len(geometryList) != len(layerNames):
            status = "The number of layers must match the number of branches"
        elif len(layerColors)!=len(layerNames) or layerColors==[]:
            status = "The number of layer colors must match the number of layers."
        else:
            sc.doc = rcdoc
            for i in range(len(geometryList)):
                currentLayer=layerNames[i]
                if layerColors==None:
                    currentColor=None
                else:
                    currentColor=layerColors[i]
                            
                #if layer does not exist, make the layer and assign layer color
                if not rs.IsLayer(currentLayer):
                    print "layer doesn't exist"
                    if layerColors!=None:
                        rs.AddLayer(name=currentLayer, color=currentColor)
                #if layer exists, check and assign layer color
                if currentColor!=None and rs.LayerColor(currentLayer)!=currentColor:
                    rs.LayerColor(currentLayer, currentColor)
                
                #get index of current layer
                layerIndex = rs.LayerOrder(currentLayer)
                
                #get objects on this branch
                for id in geometryList[i]:
                    sc.doc=ghdoc
#                    print sc.doc
                    gh_to_rhino = rs.coercerhinoobject(id, raise_if_missing=True)
                    #set object layer
                    objAttr = gh_to_rhino.Attributes
                    objAttr.LayerIndex = layerIndex
                    #separate geometry
                    objGeom = gh_to_rhino.Geometry
                    
                    #bake!
                    sc.doc=rcdoc
#                    print sc.doc
                    rcdoc.Objects.Add(objGeom, objAttr)
            status = "objects baked"
        return status
        
        
    """
    Export geometry in file to file name
    """
    def export(self, exportFP, exportFN):
        #select objects to export
        sc.doc=rcdoc
        rs.AllObjects(select=True)
        filepath = os.path.join(exportFP, exportFN)
        exportCommandString = '_-Export "' + filepath + '" _Enter _Enter _Enter'
        out = rs.Command(exportCommandString, echo=False)
        sc.doc=ghdoc
        return out
        

    """
    deletes all existing geometry from document.
    """
    def deleteExistingGeom(self):
        sc.doc = rcdoc
        allObjs = rs.AllObjects()
        rs.DeleteObjects(allObjs)
        sc.doc = ghdoc
        return
    
    
    """
    Execute Batch Export
    """
    def RunScript(self, geometry, exportFileName, exportFilePath, layerNames, layerColors, Export, deleteExisting):
        print geometry
        status = "Toggle export"
        if Export:
            if (geometry!=None) and (exportFileName!=None) and (exportFilePath!=None)\
            and (layerNames!=None) and (layerColors!=[]):
                if deleteExisting:
                    self.deleteExistingGeom()
                status = self.bake(geometry, layerNames, layerColors)
                status = self.export(exportFilePath, exportFileName)
            elif geometry==None:
                status = "Please add input geometry"
            elif exportFileName==None:
                status = "Please specify a name for your export file."
            elif exportFilePath==None:
                status = "Please specify a destination directory for your export."
            elif layerNames==None:
                status = "Please specify target layers for each branch of your geometry."
            elif layerColors==[]:
                status = "Please add layer colors."
        return status
