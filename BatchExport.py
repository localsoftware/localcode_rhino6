"""Bakes geometry into Rhino space by specified layer.
   Exports resulting Rhino file.
    Inputs:
        geometry: The geometry to bake.
        exportFileName: Export file name.
        exportFilePath: Target directory.
        layerNames: List of layer names to bake geometry into. 
        layerColors: List of colors (Optional). Can be one color or
                     as many colors as layer names. 
        Export: boolean to run component
        deleteExisting: boolean to delete geometry already in document.
    Output:
        a: None"""
        
__author__ = "jberry"
__version__ = "2019.03.14"
        
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import ghpythonlib.components as ghcomp
import scriptcontext as sc
import Rhino
import os
        
        
"""
@param    geometry       data tree of geometry
@param    layerNames     list of laye names same length as number of branches.
@param    layerColors    list of layer colors, must match length of layerNames.
        
@return   None           Adds geometry and layers to active Rhino document.
"""
def bake(geometry, layerNames, layerColors):
    geometryList = th.tree_to_list(geometry)
#    print geometryList
    if len(geometryList[0]) != len(layerNames):
        print "The number of layers must match the number of branches"
        return
    elif len(layerColors)!=len(layerNames) and len(layerColors)!=0 and \
         len(layerColors)!=1:
        print "The number of layer colors must match the number of layers."
    else:
        rcdoc = Rhino.RhinoDoc.ActiveDoc
        attr =Rhino.DocObjects.ObjectAttributes()
        sc.doc = rcdoc
        
        for i in range(len(geometryList[0])):
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
            sc.doc=ghdoc
            for id in geometryList[0][i]:
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
    rs.AllObjects(select=True)
    filepath = os.path.join(exportFilePath, exportFileName)
    exportCommandString = "_-Export " + filepath + " _Enter _Enter _Enter"
    exported = rs.Command(exportCommandString, echo=True)
    return
        
        
"""
deletes all existing geometry from document.
"""
def deleteExistingGeom():
    allObjs = rs.AllObjects()
    rs.DeleteObjects(allObjs)
    return
        
"""
Meat of the component
"""
if Export:
    if (geometry!=None) and (exportFileName!=None) and (exportFilePath!=None)\
    and (layerNames!=None):
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
        
        
        
