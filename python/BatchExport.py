"""Exports geometry to a new file.
    This component exports the branches of a geoemtry tree to files. Output files number is equal to the number of file names you input to the component. The output files can be .3dm as Rhino files, or .AI to obtain Adobe Illustrator files.  
    Inputs:
        geometry: Data tree of geometry. Each branch corresponds to a layer.
        exportFileName: Export file name.
        exportFilePath: Target directory.
        layerNames: List of layer names to bake geometry into. 
        layerColors: List of colors (Optional). Can be one color or as many colors as layer names. 
        Export: boolean to run component
        deleteExisting: boolean to delete geometry already in document."""

__author__ = "jberry"
__version__ = "2019.05.24"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System, Rhino, os
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import ghpythonlib.components as ghcomp
import scriptcontext as sc
rcdoc = Rhino.RhinoDoc.ActiveDoc
ghdoc = sc.doc

class MyComponent(component):
    
    def RunScript(self, geometry, exportFileName, exportFilePath, layerNames, layerColors, Export, deleteExisting):
                
        def bake(geometry, layerNames, layerColors):
            geometryList = [geometry.Branch(b) for b in range(geometry.BranchCount)]
        #    print geometryList
            if len(geometryList) != len(layerNames):
                print "The number of layers must match the number of branches"
                return
            elif len(layerColors)!=len(layerNames) or layerColors==[]:
                print "The number of layer colors must match the number of layers."
            else:
                attr =Rhino.DocObjects.ObjectAttributes()
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
                        gh_to_rhino = rs.coercerhinoobject(id)
                        
                        #set object layer
                        objAttr = gh_to_rhino.Attributes
                        objAttr.LayerIndex = layerIndex
                        #separate geometry
                        objGeom = gh_to_rhino.Geometry
                        
                        #bake!
                        sc.doc=rcdoc
                        rcdoc.Objects.Add(objGeom, objAttr)
            return
                    
        
        """
        Export geometry in file to file name
        """
        def export():
            #select objects to export
            sc.doc=rcdoc
            rs.AllObjects(select=True)
            filepath = os.path.join(exportFilePath, exportFileName)
            exportCommandString = '_-Export "' + filepath + '" _Enter _Enter _Enter'
            out = rs.Command(exportCommandString, echo=True)
            sc.doc=ghdoc
            return
                
                
        """
        deletes all existing geometry from document.
        """
        def deleteExistingGeom():
            sc.doc = rcdoc
            allObjs = rs.AllObjects()
            rs.DeleteObjects(allObjs)
            sc.doc = ghdoc
            return
                
        """
        Meat of the component
        """
        if Export:
            if (geometry!=None) and (exportFileName!=None) and (exportFilePath!=None)\
            and (layerNames!=None) and (layerColors!=[]):
                if deleteExisting:
                    deleteExistingGeom()
                bake(geometry, layerNames, layerColors)
                export()
            elif geometry==None:
                print "Please add input geometry"
            elif exportFileName==None:
                print "Please specify a name for your export file."
            elif exportFilePath==None:
                print "Please specify a destination directory for your export."
            elif layerNames==None:
                print "Please specify target layers for each branch of your geometry."
            elif layerColors==[]:
                print "Please add layer colors."

        return 
