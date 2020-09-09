from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System, Rhino, os
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import ghpythonlib.components as ghcomp
import scriptcontext as sc
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML
rcdoc = Rhino.RhinoDoc.ActiveDoc
ghdoc = sc.doc


class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Bake with Attributes", "BakeWithAttributes", """Bakes geometry with attributes into Rhino.
The geometry is baked by branch into specific layers.
Geometry objects can have colors, widths, and materials as attributes.
You can group the baked objects and delete all the previous instances of the objects.
    Typical usage example:
Input geometry an separate (graph) them into branches of a data tree.
Provide a list of layer names to each branch that will be baked. Input all the desired attributes.
Use a 'make Material' LocalCode component to make and assign a material to each layer.
Toggle the 'Bake' boolean to activate the component.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("19ed4779-7e63-46a2-9560-1ccf4600e90c")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "geometry", "geometry", "Geometry as a tree of objects")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "layers", "layers", "Layer names as a list of strings")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "colors", "colors", "Color swatches as a list")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "widths", "widths", "List of floats")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "materials", "materials", "List of LocalCode Materials")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "delete", "delete", "Boolean to delete 'EVERY' previous instance of the geometry")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "group", "group", "Boolean to group all objects")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "Bake", "Bake", "Boolean that bakes the geometry with attributes into Rhino")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        pass    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        p5 = self.marshal.GetInput(DA, 5)
        p6 = self.marshal.GetInput(DA, 6)
        p7 = self.marshal.GetInput(DA, 7)
        result = self.RunScript(p0, p1, p2, p3, p4, p5, p6, p7)

        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAEnQAABJ0Ad5mH3gAAASESURBVEhLzVR9TNR1GCfwjoMD7o6Dg3jzkBfxeI9LuOOOu4MDTOaqRa1mZkRqaqzRpmFNbVNrmraMXtBFpdVyTaOmRW7oyLks1ppazA1IaJm8OYo8eRP49Dzf71Emx3pZf/TZPvv9fs/3eT7P8/s+z/fr939GNLFGrw9qVIcqX6P3lcRwXvgvUFWxxDDYfCwXvT2F+KHDig/ez8KSUkMvrT0qXf49tm3fmgKgmOgCJoqA6w75Trbnnk0G+WySrv8cO+r3pJFQCTBql+JTJD5Kz1/pm59wo2ZNAiexy5C/ByVxx0u7Fkrx6yzkwkC3FV3n8zHxs/zGVZnUM1iEhLjgUzLUN7KIGzQaZUNCgvpIiUvfeeidTBKhbSHxq1eKUPVQHGgdAQH+SE0OwYE30v9IQkU8WTOf/2KRULsJzz+2KmHqdKsZlzqtGL5so6qcMviaHdMTLlSUGzh4Fpuo0bIXThz/OIdta4g34pYXDuznStzCSWzFOJGERWXTTnzRkjdLeIbmXC2mxylu2oGedgtUKsUrZP8d7rraRCnu8QreTKrurQaTT3FmZIQKowPkRwmGf7IhPi74MNklEo3qM6ND3op9iTPpr1qbc32KM7PSwzA1Rn9AjR4ZtCM1JeQo2QUyNtYaSYAmhMfNlzhzxI7JUSfslnCfCQ6K7aUejNEg9NqQaAxuIrvAupZjOaJCn8KclNcoEBMODPxow7KKKJqgACEcZVDhxZ08wiTO20u96+2yIixM2SjUAwMVey9+VyAPja8EYw4ceS8LwocPE5/cKRc6zuaj7XMzhi7RpM2Isz8Vw3aSrhMJtFplY9/3FlGdqJanRowbXwdUOb1nmHRobsql91KZhMXEOk8c+d64tWSv372QExSLBEql4uXumT8g8UmPA1vqFtDlFYETn7CoG+VuA2wWPVaviqeTKgs4/G4mlpZF4LOPsinWu73exOUlEf0krRYJCOtb6GacqfbN100wpYXhibXzkZIcCky64bTrkZejQTrZNz+VKPqg1ajwwH0x0OmCcIW3iXtEZ6W9bTH3Z69XW8DER1tMEY3phbMF2FCbhPsro2FMUFOgC86iCHxzOo/2Ng9lxZFiYvhEA2VkN+NaPyXgC5A0Ku+KHidNo5T2IubWoJO/9EqHXduTkb6I/mCdEWmpYSKBqygS335lRlsrJSiJxNsN6Vi2NIr8y/Hph9no5x5SLF8XJLdZqv4Z5qoHY8npDqytjoU1PxzVdKH5+/tjyuOka0AHy2IdcjI12LppAS53F0KnVWF1dTzUwYHwDDlw4ZyFT/NJ0vKXkrPx+LYtSRjud2DF8mg8siIWz2xMhKfPhn31abjnTgNWLo/BCJ946tXB/SaUFofjzKnbce5rC29nG2lopdTceLjy7uihjnYriZR5yc3nkaQeCfI3k9fc2PeqCSHB8w5RbKiU+GvE881aXhbZs3NHKk7Q/dN5vgB9F62CHfR+/Ggunq5LQnaG5kvyv1eGzYLV+5wTQcRC4nqFQrFHr1c1MgMUAbvJxnf9bcS5MM/Pz6/rN3O1kPdwDpc/AAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, geometry, layers, colors, widths, materials, delete, group, Bake):
        #Call rhino document 
        rcdoc = Rhino.RhinoDoc.ActiveDoc
        #Make a list of the geometry branches
        geometryList = [geometry.Branch(b) for b in range(geometry.BranchCount)]
        #Check if the number of layers is the same as the branches
        if geometry == None:
            self.AddRuntimeMessage(RML.Warning, "Add geometry in branches.")
        if Bake == None:
            self.AddRuntimeMessage(RML.Warning, "Add a boolean toggle in the Bake input.")
        if len(layers) != geometry.BranchCount:
            self.AddRuntimeMessage(RML.Warning, "Add the same number of geometry branches and layers.")
            
        if Bake:
            
            if delete:
               for i in range(len(layers)):
                sc.doc = rcdoc
                if rs.IsLayer(layers[i]):
                    allObjs_l = rs.ObjectsByLayer(layers[i])
                    rs.DeleteObjects(allObjs_l)
                sc.doc = ghdoc
                    
            num = len(geometryList)
            for i in range(num):
                currentLayer = layers[i]
                if colors != [] and len(colors) == num:
                    currentColor = colors[i]
                else:
                    currentColor = [0,0,0] 
                if materials != [] and len(materials) == num:
                    currentMaterial  = materials[i]
                else: 
                    currentMaterial = None
                if widths != [] and len(widths) == num:
                    currentWidth = widths[i]
                else: currentWidth = 1.0
                                
                for id in geometryList[i]:
                    sc.doc = ghdoc
                    gh_to_rhino = rs.coercerhinoobject(id)                
                    attributes = gh_to_rhino.Attributes
                    geometryObj = gh_to_rhino.Geometry
                    sc.doc = Rhino.RhinoDoc.ActiveDoc #we change the scriptcontext           
                    rhino_brep = sc.doc.Objects.Add(geometryObj, attributes)#we add both the geometry and the attributes to the Rhino doc
                    if(group):
                        name = rs.AddGroup('bake_group')
                        rs.AddObjectToGroup(rhino_brep, 'bake_group')
                
                    if not rs.IsLayer(currentLayer) and currentColor != None:
                            rs.AddLayer(name=currentLayer)
                            
                    prevColor = rs.LayerColor(layer=currentLayer)
                    if prevColor != currentColor: 
                        rs.LayerColor(currentLayer, color = currentColor)           
                
                    index = rs.LayerOrder(currentLayer)
                    if currentMaterial != None:
                        #print(currentMaterial.Name) 
                        sc.doc.RenderMaterials.Add(currentMaterial)                    
                        sc.doc.Layers[index].RenderMaterial = currentMaterial
                                        
                    rs.LayerPrintWidth(currentLayer, float(currentWidth))     
                    rs.ObjectLayer(rhino_brep, currentLayer) # add objects to rhino layer                    
        sc.doc = ghdoc #we put back the original Grasshopper document as default
                
                                    
                
                
        
        # return outputs if you have them; here I try it for you:
        return 


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Bake with Attributes"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("3ac6d17f-7e16-4c11-ad4c-4b82e1f6e54b")