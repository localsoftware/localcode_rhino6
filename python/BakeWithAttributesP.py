from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System, Rhino, os
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import ghpythonlib.components as ghcomp
import scriptcontext as sc


class MyComponent(component):
    
    def RunScript(self, geometry, layers, colors, widths, materials, delete, group, Bake):
        result = geometry
        geometryBranchesNum = geometry.BranchCount
        
        geometryList = [geometry.Branch(b) for b in range(geometry.BranchCount)]

        if len(layers) != geometryBranchesNum:
            print "Add same number of layers and geometry branches"
        elif len(colors) != geometryBranchesNum:
            print"Add same number of colors and geometry branches"
        elif len(materials) != geometryBranchesNum:
            print"Add same number of materials and geometry branches"
        elif len(widths) != geometryBranchesNum:
            print"Add same number of widths and layers"
        
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
                currentWidth = widths[i]
                

                
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
                    
                    if rs.LayerPrintWidth(currentLayer)!= None:
                        rs.LayerPrintWidth(currentLayer, float(currentWidth))
                    else:
                        rs.LayerPrintWidth(currentLayer, 1.0)
                    
                    rs.ObjectLayer(rhino_brep, currentLayer) # add objects to rhino layer
                    
                    sc.doc = ghdoc #we put back the original Grasshopper document as default
                    

        # return outputs if you have them; here I try it for you:
        return result
