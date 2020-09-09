"""Bakes geometry with attributes into Rhino.

The geometry is baked by branch into specific layers.
Geometry objects can have colors, widths, and materials as attributes.
You can group the baked objects and delete all the previous instances of the objects.

    Typical usage example:
        Input geometry an separate (graph) them into branches of a data tree.
        Provide a list of layer names to each branch that will be baked. Input all the desired attributes.
        Use a 'make Material' LocalCode component to make and assign a material to each layer.
        Toggle the 'Bake' boolean to activate the component.

    Inputs:
        geometry: Geometry as a tree of objects
        layers: Layer names as a list of strings
        colors: Color swatches as a list
        widths: List of floats
        materials: List of LocalCode Materials
        delete: Boolean to delete 'EVERY' previous instance of the geometry
        group: Boolean to group all objects
        Bake: Boolean that bakes the geometry with attributes into Rhino

    Outputs:
        None"""

__author__ = "palomagr"
__version__ = "2020.07.09"

# ghenv.Component.Name = "Bake with Attributes"
# ghenv.Component.NickName = "Bake with Attributes"


from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System, Rhino, os
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import ghpythonlib.components as ghcomp
import scriptcontext as sc
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML


class MyComponent(component):

    def RunScript(self, geometry, layers, colors, widths, materials, delete, group, Bake):
        # Call rhino document
        rcdoc = Rhino.RhinoDoc.ActiveDoc
        # Make a list of the geometry branches
        geometryList = [geometry.Branch(b) for b in range(geometry.BranchCount)]
        # Check if the number of layers is the same as the branches
        if geometry == None:
            self.AddRuntimeMessage(RML.Warning, "Add geometry in branches.")
        if Bake == None:
            self.AddRuntimeMessage(RML.Warning, "Add a boolean toggle in the Bake input.")
        if len(layers) != geometry.BranchCount:
            self.AddRuntimeMessage(RML.Warning, "Add the same number of geometry branches and layers.")

        # Function that deletes all previous instances of the geometry
        def deleteExistingGeom():
            sc.doc = rcdoc
            allObjs = rs.AllObjects()
            rs.DeleteObjects(allObjs)
            sc.doc = ghdoc
            return

        if Bake:
            if delete:
                deleteExistingGeom()

            num = len(geometryList)

            for i in range(num):
                currentLayer = layers[i]
                if colors != [] and len(colors) == num:
                    currentColor = colors[i]
                else:
                    currentColor = [0, 0, 0]
                if materials != [] and len(materials) == num:
                    currentMaterial = materials[i]
                else:
                    currentMaterial = None
                if widths != [] and len(widths) == num:
                    currentWidth = widths[i]
                else:
                    currentWidth = 1.0

                for id in geometryList[i]:
                    sc.doc = ghdoc
                    gh_to_rhino = rs.coercerhinoobject(id)
                    attributes = gh_to_rhino.Attributes
                    geometryObj = gh_to_rhino.Geometry
                    sc.doc = Rhino.RhinoDoc.ActiveDoc  # we change the scriptcontext
                    rhino_brep = sc.doc.Objects.Add(geometryObj,
                                                    attributes)  # we add both the geometry and the attributes to the Rhino doc
                    if (group):
                        name = rs.AddGroup('bake_group')
                        rs.AddObjectToGroup(rhino_brep, 'bake_group')

                    if not rs.IsLayer(currentLayer) and currentColor != None:
                        rs.AddLayer(name=currentLayer)

                    prevColor = rs.LayerColor(layer=currentLayer)
                    if prevColor != currentColor:
                        rs.LayerColor(currentLayer, color=currentColor)

                    index = rs.LayerOrder(currentLayer)
                    if currentMaterial != None:
                        # print(currentMaterial.Name)
                        sc.doc.RenderMaterials.Add(currentMaterial)
                        sc.doc.Layers[index].RenderMaterial = currentMaterial

                    rs.LayerPrintWidth(currentLayer, float(currentWidth))
                    rs.ObjectLayer(rhino_brep, currentLayer)  # add objects to rhino layer
        sc.doc = ghdoc  # we put back the original Grasshopper document as default

        # return outputs if you have them; here I try it for you:
        return
