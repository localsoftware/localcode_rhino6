from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "DeleteAll", "DeleteAll", """Deletes all geometries of Rhino document.
Deletes the Rhino geometry created by GH components.
This is useful for batch processing multiple files.
    Typical usage:
Toggle a boolean in the 'Delete' input to erase the all the objects.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("efa55a42-046e-45fa-aa24-324b5dd9e8da")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "Delete", "Delete", "boolean delete")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        pass    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAALwSURBVEhL7ZbLS1RRHMf9F2rTS6UgFy5sPHfm3PedGTWwh6YlqbQSjFq0ECoiSWN6OFEapWGPXW1q1SYiyNEeKmOJkgUlRCBCJfRQHE2nx8y337mjzDgzaQuDoBZf5p7f+d3v5577u+d3JiM6bW2PRgvPRafM5Rf5CkA7UAyg8A+oGBmCZA+mrLimE/TdwuR7CyMvPRgdjkuMJ9667fkF+Yk+5BsHhCgwK4LipjnR9WDQhK45wSQXXNwFPieJxrLsRHfASLkHYfIRfgsAZD5BT3qiUUHFTo7dFRxV1ZxMXFi1hmH9BilFq9dKNkjkVVL+rnKOxnoF4+/mHzYRQOTr11T7poajMvynOfw+jhY/x6XzMtpaUiXiLWcol/L8pzh8DTIysyVcvqjGVpIMuNisYGOOEx9GTERnDUQmUxUNpY9HZgyExkxscrhw8ricBvDDjeBDAw6HBE1l0HUGiTGoCoPbYmB0zTmDx83gcsXGFsVFrsjTNSEJubkSAnepLpFkgKg6FWn0tQWvl6OsVEZnp4W6Axry8iR03DHQfkGx3/3VNgOBezqBnNhbo6KL8vZUK3bRhwdN8iGvlK9IBL6IoBflZRz7ahW6LsCVVhP5+QyIujEUVLAuk+HVoIfmLPuJm3y6nXfkkIrNRc6YuSjwLwFhD3aUctTWCIAXrc2GDYhMWgh2KcjKZhjoEZ+i+Hwl+I4JgBcH61QUFjipRuQx8x/wjwFCfwHA4YgDMrPiAE1dBkBzk4GcnBig+76CFSsZnjyKAURbqT+8ZA2ss8mA0hKO/fZO9uLjqBvP6EwQO/nbuIX+xybBxE5248VTE2NvCEZ5Yid7Pb+zgq8ebN3CUbKNo7dHR3+3hud9GnoCGvoeaGQqflX0dGgYovgAzff26qiqlKkREkCcagtXkAAQoq56+6ZOHdRJnTQfGnXJpSTyTEPCrRta7FSb90oLmIOEP5t0Fosev7REXvgTvUbRohN9bMCi/yqK0mixeLKK8RNsEwh51DlQPwAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, Delete):
        if Delete == None:
            self.AddRuntimeMessage(RML.Warning, "Add a boolean toggle in the Delete input.")
        if Delete:
            rcdoc = Rhino.RhinoDoc.ActiveDoc
            sc.doc = rcdoc
            allObjs = rs.AllObjects()
            rs.DeleteObjects(allObjs)
            sc.doc = ghdoc    
            # return outputs if you have them; here I try it for you:
            return 


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "DeleteAll"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("779d145c-9d7b-4705-81d3-d091cdf8114d")