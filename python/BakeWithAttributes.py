"""Bakes geometry with attributes.

This component bakes the geometry of a file into Rhino geometry with the attributes that you assign to them. 

    Typical usage example: you design a series of geometries with the LocalCode components and bake them into Rhino as objects with attributes. 'Bake' is the boolean that activates the component to bake.

    Inputs:
        geometry: Geometry as a tree
        layers: Layer names as a list
        colors: Colors swatches as a list
        widths: List of floats
        materials: List of LC Materials 
        delete: Boolean to delete 'EVERY' previous instance of the geometry
        group: Boolean to group all objects
        Bake: Instanciates geometry with attributes to Rhino
        
   Outputs:
        Baked series of geometries with attributes in Rhino. 
  
"""

__author__ = "palomagr"
__version__ = "2020.07.09"

#ghenv.Component.Name = "Bake with Attributes"
#ghenv.Component.NickName = "Bake with Attributes"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System, Rhino, os
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import ghpythonlib.components as ghcomp
import scriptcontext as sc


class MyComponent(component):
    
    def RunScript(self, geometry, layers, colors, widths, materials, delete, group, Bake):
        geometryBranchesNum = geometry.BranchCount
        
        geometryList = [geometry.Branch(b) for b in range(geometry.BranchCount)]

        if len(layers) != geometryBranchesNum or len(colors) != geometryBranchesNum or len(materials) != geometryBranchesNum or len(widths) != geometryBranchesNum:
            print"Add same number of geometry branches and lists of attributes"
            
        
        def deleteExistingGeom():
            sc.doc = rcdoc
            allObjs = rs.AllObjects()
            rs.DeleteObjects(allObjs)
            sc.doc = ghdoc
            return
            
            
        rcdoc = Rhino.RhinoDoc.ActiveDoc
        ghdoc = sc.doc
        groupName = '' #empty string for group name
        
        if Bake:
            
            if delete:
                    deleteExistingGeom()
            #we obtain the reference in the Rhino doc
            for i in range(len(geometryList)):
                currentLayer = layers[i]
                currentColor = colors[i]

                currentMaterial = materials[i]
                
                if widths != []:
                    currentWidth = widths[i]
                else: currentWidth = 1.0
                

                
                for id in geometryList[i]:
                    sc.doc = ghdoc
                    gh_to_rhino = rs.coercerhinoobject(id)                
                    attributes = gh_to_rhino.Attributes
                    geometryObj = gh_to_rhino.Geometry
                    #we change the scriptcontext
                    sc.doc = Rhino.RhinoDoc.ActiveDoc            
                    #we add both the geometry and the attributes to the Rhino doc
                    rhino_brep = sc.doc.Objects.Add(geometryObj, attributes)
                    
                    if(group):
                        name = rs.AddGroup('bake_group')
                        rs.AddObjectToGroup(rhino_brep, 'bake_group')
                    
                    if not rs.IsLayer(currentLayer) and currentColor != None:
                            rs.AddLayer(name=currentLayer, color = currentColor)
                    index = rs.LayerOrder(currentLayer)

                    sc.doc.RenderMaterials.Add(currentMaterial)                    
                    sc.doc.Layers[index].RenderMaterial = currentMaterial
                    
                    rs.LayerPrintWidth(currentLayer, float(currentWidth))     
                    rs.ObjectLayer(rhino_brep, currentLayer) # add objects to rhino layer                    
                    sc.doc = ghdoc #we put back the original Grasshopper document as default
                    

        # return outputs if you have them; here I try it for you:
        return 
