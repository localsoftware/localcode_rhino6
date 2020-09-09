from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython, System, Rhino
import rhinoscriptsyntax as rs
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "SHPExtractUserStrings", "SHPExtractUserString", """Extracts object attribute names and attribute values from geometries imported from SHP files.
Extracts the User Strings from geometries imported with the ReadShapefile component.
Separates the GIS Attributes into DataTrees for every GIS geometry from the shapefile.
Based on the work of Jackie Berry.
    Typical usage:
Connect the output geometry from a ReadShapefile component into the geometry input.
You can plug a panel to the Attributes and Values outputs to browse their specific values.
You can select the values of specific geometries with any List Management component, such as List Item.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("9e155ce4-692c-48f0-8a2e-efe279bb779b")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Geometry()
        self.SetUpParam(p, "geometry", "geometry", "imported geometry from shapefile.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Attributes", "Attributes", "Tree of attributes per object from shapefile")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Values", "Values", "Value per attribute per object from shapefile.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAALbSURBVEhL5ZVrSJNRGMeX07m5DZNVbo285KQx3UYapYW7BfWlRCmKzMoun0IIP5iQmQVFVtLtQyCIH8Kii1LgBwmjBAkiCCzDNMgoKMigcs5Lrvb0f847cy9Kudq3/vDjvOe8z+19ztmZ4r9TCtisVCqbMR4Hal78V6WDCoMhsa140+Lhy+etNNBXSHduOcluTe7HuxJhFaUcoNqSqX+4u9w4fv1qLn0YWkdEPomQG6OXAl/cdKw2i/RJ8e2wXyE851Ac0AEPOJOfl9J7qDKd7nWspNHhonBQL1HQRfTdQ4GPWMNIoxi/YY3WU/+zAtpSsmQM/vVAA2SyKJVxr+tqsuh57xoKBbg6DoogkwjAgQJFFJryUE1VBpmMGmo4YZlJwpDk037TSU578kvELJVCh4VNK95aahyZ8MOJq/WHHaeZcFFwxE06rYpgTmnLtERTsBuLsEER7Dv+1U0Np7LJZtXfhe1qkSAsR45N92YQGyiSRCZggh5quWIjT5GB2lrtYi57z8n4q9Gyz8NuKttm5mK6pdAzMi81JT3pebAKhmhTZACGA4SQnMfpr+Q2sm3QS91d+bSzzDip16luIJYP8P7OklatTui4fc0hqpG1geFW8PhD6rv/k4tamnLI7TK8he9JYBFR/qwFTZcarVIS7IGo+FcbfPTqRQEdqVlO2ZakRzCuAHwSo1b94apMEVCAjb3fmUc7tqeOazSqVrx3SWbzV3x4jNSBveVmam7KpbWFhiHM+YrIFG+i1ELAZ9gmZnJtALvAXAXMW/uBH5wWM4UiFfA9lAY4OffYFJ7z+u9YBGbpMeDL6z3QgoOgEZyLEvbZA2TaCHoAV80XVx2IqXjTMqRHRSJwSo+xkxl0Aa6+mhdirXwwCI6CPpAAVID/sf4G9peJW8IJzoKngPeiElwEF6KEffYBmfgL3oFaMAD4qPFFxedeGSXsM+uS4zPOPySu2s4LsZFC8RMzO7R6gUkDrAAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))


    def RunScript(self, geometry):
        Attributes, Values = None, None
        if geometry == None: 
            self.AddRuntimeMessage(RML.Warning,"add geometry.")
        else:
            data = geometry.GetUserStrings()
            d = {}
            k = []
            v = []
            for u in data:
                k.append(u)
                d[u] = data[u]
                v.append(d[u])
            U = d
            Attributes = k
            Values = v
        # return outputs if you have them; here I try it for you:
        return (Attributes, Values)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "SHPExtractUserStrings"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("9581a34a-e80f-4b59-ab15-0c7b382a8bfa")