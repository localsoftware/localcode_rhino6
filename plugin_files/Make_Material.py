from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Grasshopper as gh
import scriptcontext as sc
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "MakeMaterial", "MakeMaterial", """Creates a new Material.
Returns a new Material, a Render Material and a GH Preview Material using the parameters set as inputs.
To bake into Rhino you need to use the 'Bake with Attributes' LocalCode component. The material will be baked into a layer.
Based on the work of Chris Hanley.
    Typical usage:
Input a name and a diffuse color and create a material.
The rest of the inputs are optional.
Use the 'Material' output to assign the material to a geometry.
Plug the 'GHMaterial' output to a 'Preview' component to visualize your material on GH objects.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("d618faec-c27e-4411-bae2-3c3c9942dc3f")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "Name", "Name", "name string")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Colour()
        self.SetUpParam(p, "diffuseColor", "diffuseColor", "diffuse color")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Colour()
        self.SetUpParam(p, "specularColor", "specularColor", "specular color")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Colour()
        self.SetUpParam(p, "emissionColor", "emissionColor", "Script input emissionColor.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "transparency", "transparency", "transparency from 0 to 1")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "reflection", "reflection", "reflection range from 0 to 1")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "glossiness", "glossiness", "glossiness from 0 to 1")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "Make", "Make", "Script variable Make Material")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Material", "Material", "Render material for Rhino geometry")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "GHMaterial", "GHMaterial", "Material for GH preview ")
        self.Params.Output.Add(p)
        
    
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

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAAOUSURBVEhLtZbZTxNRFMb9Q1RAFpGWttMp1UJnwELD0ooxqCHiQkoiGhN54MEGTIz6AsoDPhiXxMREjFvUKGA0IUGJij6QiLKDUASNC8Fgcdd+nnNpsa1DNUYfvkznztzv951z7810UWBWcQUCjkMBv/3fi3wZcBTIB+D4D8rHIiaJG78SW7OkD6SPpPfBsd+JfGMD3pE+kUD6bIP/pYwpn4T3r2S6X0nj9jmo1lxWTAAnhorXzyw4ddyAWq8TNd5tOLB/Nw7u347DdcW4dsmKGYZxgOj5rAUB3AKadKEpHZs3F6Ou/iTab3ehp2cEg4Nj6O19inv3e9DU1ILamnK03zLS+1QNhwr30QSI5AqONJjgqajGo+5BTEw8w8DAABn3EqRHqK+vD2NjY3j8ZBTV1Xtx6SxDgh4LArjn1JaLZ0woLCqjtCMYHh7G6OioUH9//zwgJAYPDflQXr4Tne1mIBAL8FnB9PMsqIoFLncJKio88Hg88Hq91I4mdHd3Y3x8nMCDERCu5Nz5Fmxcn4Gvs2EL/wuA0p86ZoVOr6KoqAi5ublwOBxQVVWotLQUDQ0N6OzshM/nE20KVdHV1QWzvBptzRlUhaoB4N5/UbG1zAyjKQtutxuFhYURysvLg91uF88aGxupNUMi/eTkJDo6OpCYJKN2D7WJgv4KoAP04bUduQ4zVqwwiuRsxJVEg5xOpwBVVVWhubkZbW1tqKysxOIly7Flk0W0em6zhAPoQE1P2KHYZaSlGZCeni5MCgoK4HK5NBVqnyRJSElJoWBmlKwjAJuLra5RQZ5Dhk4nwWg00lUnrlarVcCys7ORk5MDRVGQmZkpxg0GA/R6PcxmM5anSjEqEGugoHyrhdJIYgKL05lMpggxlMW/+R1ZlsU1YZmEfbXWBdYguItOn1iFpXESTZoD/KkYFp9gxJ2bmVG76F0YgEp7+yK0DtpGWuIwSUkSNpRY8I3PQMQ5CAcET3LrZRulkWAwahuGi811Ot55Eh49yPqZXhPAEouj4uTRVUggCO8MLeOQkmm9UmlxW6/axLx5n3mAX6mPALDEFlNx47qNtqKMuHgJScmSaJtOT2npmpgoiQDFayx4eJf6Hm3O0qwgpGAl/jcKzp+xYdeODBS7Lch3yli31oLqKitartjwVRhpmItxUcECANb8F40MqLffZxR8mgo+4zHWX3/RosUVsRl/k2OZhksA/uu/inz8AJMCHHwHHr5bAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))


    def RunScript(self, Name, diffuseColor, specularColor, emissionColor, transparency,
                  reflection, glossiness, Make):
        GHMaterial = None
        Material = None
        
        if Name == None:
            print("Add a Name")
            self.AddRuntimeMessage(RML.Warning,"Add a Name string")
            
        if diffuseColor == None:
            print("Add a diffuse color")
            self.AddRuntimeMessage(RML.Warning,"Add a diffuse color")
        if Make:

            for mat in Rhino.RhinoDoc.ActiveDoc.RenderMaterials:
                if mat.Name == Name:
                    Rhino.RhinoDoc.ActiveDoc.RenderMaterials.Remove(mat)#deletes the previous material
            newMat = Rhino.DocObjects.Material()
            newMat.Name = Name
            newMat.DiffuseColor = diffuseColor
            newMat.AmbientColor = diffuseColor
            
            
            
            
            if specularColor != None:
                newMat.SpecularColor = specularColor
                newMat.ReflectionColor = specularColor

            if emissionColor != None:
                newMat.EmissionColor = emissionColor
            
            if transparency != None:
                newMat.Transparency = transparency
            else: 
                newMat.Transparency = 0

            if glossiness != None:
                Smoothness = min(max(glossiness, 0), 1);
                newMat.ReflectionGlossiness = Smoothness
            else:
                newMat.ReflectionGlossiness = 0
                
            if reflection != None:
                Reflection = min(max(reflection, 0), 1);
                newMat.Reflectivity = Reflection
            else:
                newMat.Reflectivity = 0


            Material = Rhino.Render.RenderMaterial.CreateBasicMaterial(newMat)
            GHMaterial = gh.Kernel.Types.GH_Material(Material)  # GH preview material


        # return outputs if you have them; here I try it for you:
        return (Material, GHMaterial)

import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "MakeMaterial"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("7f29287f-2f5a-470b-80ed-8b7b33b59666")