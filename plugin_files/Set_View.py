from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython, System, Rhino, os
import rhinoscriptsyntax as rs
import cPickle as pickle
from scriptcontext import doc
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "SetView", "SetView", """Set the current Rhino viewport to a camera view.
Once you have a camera created, the Set View component easily adjusts the view to it.
You can use these views to batch render, export or create presentation drawings from GH geometries easily.
Based on the work of Jackie Berry.
    Typical usage:
Once you have created a view with the Create View component, simply plug the Geometry, View Vector,
and View Target outputs into the geometry, vector, and target inputs of the component.
Once you have a view created, you can easily adjust the view with it. You can use these views to batch render.
Add a Boolean Toggle component to activate and deactivate the view change.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("6350cbdf-02db-4780-bf4f-7b85ae0c13e7")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "setView", "setView", "boolean to set view")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Geometry()
        self.SetUpParam(p, "geometry", "geometry", "geometry in view")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Point()
        self.SetUpParam(p, "target", "target", "3D point defining camera target")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "vector", "vector", "3D vector defining camera direction")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        pass    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        result = self.RunScript(p0, p1, p2, p3)

        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAAJUSURBVEhL7ZNfSJNRGMY3RzbDisaam6wahZkkazm9aO3Trcmiiy4kCOoiMaGgvwhFV9FNRAVdRReJdxX9oWIIgauoi1kEFdRFFxkFkhczRkUqWmZPzzkf38e+dXQys6sO/Nh2zvs+z3nf8872r9ZacnweiBC5dh89EEA63Yi+VGju9IVx4UwNqHtOl7fZdlztWQ8gSWIlEC/43YpXTxuEwSldngbdF+t4sAUY0WbHNyLEpshIs547wU+5H0fm/oYZDESQCEaL/l0l/iuG5/1NaI27sa62Eof2r8TYZ+aMi7xiBgwazUbxMtPEGypMvjfj08co3C6nEDHZ17FCis9sMEoBJNDZ7ofD4cDg24hukm9AgdSNeou4oGq5E5NfilVA7t0OmUnbkh59fyzPgO15kWk0Yww2BpdiakI8ssLgsjRIIDekocpjLf1Kt5gwmhitElX+jKHrcMCMcS1biMfpBv3RVQY9l4TBVrRt95pJBiJ5eDBK0bxWiYoo9uxRGHeuBTE0sIn5YqK4rzLovRlE7y25qWRnm4+JCf32hol8L3Fj0Vqe8fFllSqDY0fWwOe1tqaQ1PWgLma0So5rC8ZzGk6eWI3sew6EqFJlYLeX/SFYSLW3Al+HKfrDuGkMuawGbbNLnov/BCZFNQoDYhGbjs49fgqwHRT5wBGur1tiOe86uIpnSfQ/KNFA8ORhGANvIvD7KpTnd9nKd6/lGJdm4K9eBI97+vdaXLkA50/XwOksK81gdthRXj6vBpL/BkUxDXYRVcBcOUvkCpC9pOMvQj1b6DcWHnK9ANPuOgAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))


    def RunScript(self, setView, geometry, target, vector):
        if geometry == None :
            self.AddRuntimeMessage(RML.Warning,"Add target geometry.")
        if setView == None :
            self.AddRuntimeMessage(RML.Warning,"Add a boolean to set the view.")
        if target == None :
            self.AddRuntimeMessage(RML.Warning,"Add a target as a 3D point.")
        if vector == None :
            self.AddRuntimeMessage(RML.Warning,"Add a vector.")
        if setView:
            vp = doc.Views.ActiveView.ActiveViewport
            vp.SetCameraDirection(vector, True)
            vp.SetCameraTarget(target, True)
            bb = rs.BoundingBox(geometry)
            rs.ZoomBoundingBox(bb)
            doc.Views.ActiveView.Redraw()
        return


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "SetView"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("bcbd4b9f-f803-47dc-823c-cfe5961bf8d1")