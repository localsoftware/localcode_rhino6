"""Deserializes data from binary file.

Un-pickles (de-serializes) pickled files into Grasshopper geometries.
Un-pickling geometry is faster and more efficient than importing Rhino files.
Based on the work of Jackie Berry.

    Typical usage:
        You need to provide a path for the folder that contains the files to be imported.
        Use the string concatenate component to join the file path of the folder with the number of the file to be imported.
        You can specify the file number with a slider. Specify the name of the layers you want to import from the rhino file.
        Type the layer names in a Panel. Make sure the Multiline Data option is unchecked (you can uncheck the box while typing in the panel or by right click).

    Inputs:
        siteNumber: site number
        layer: layer name
        path: path to source file directory.
        read: boolean

    Outputs:
        geometry: converted geometry"""

__author__ = "palomagr"
__version__ = "2020.07.09"

#ghenv.Component.Name = "Unpicke Data"
#ghenv.Component.NickName = "Unpickle Data"

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython, System, Rhino, os
import rhinoscriptsyntax as rs
import cPickle as pickle
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "UnPickleData", "UnPickleData", """Deserializes data from binary file.
Un-pickles (de-serializes) pickled files into Grasshopper geometries.
Un-pickling geometry is faster and more efficient than importing Rhino files.
Based on the work of Jackie Berry.
    Typical usage:
You need to provide a path for the folder that contains the files to be imported.
Use the string concatenate component to join the file path of the folder with the number of the file to be imported.
You can specify the file number with a slider. Specify the name of the layers you want to import from the rhino file.
Type the layer names in a Panel. Make sure the Multiline Data option is unchecked (you can uncheck the box while typing in the panel or by right click).""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("9ee7b433-de34-4fe0-be43-bf9858f66520")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "siteNumber", "siteNumber", "site number")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "layer", "layer", "layer name")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "path", "path", "path to source file directory.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "read", "read", "boolean")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "geometry", "geometry", "converted geometry")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        result = self.RunScript(p0, p1, p2, p3)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAAO5SURBVEhL3ZRrTBRXFMeXZZzlsSwy67AoIOAuu8rCIrZawAV2pU01GjXRRE3VanwbhbTBR7Rp2sa2toqEIK1awEcQEB+BxEf0A03TNDXxERtUYnz0QzFBRdcHiqzQf8+dcR8DszWN33qSX3b2nnP+/zt37r2a/03oiU2iGHkkMTG6lWh5C1oFQddIeqWEjolrTaaIM61Hs3Gv0wnPXYL9/kce+/rot6tzMhr2ZyIulq9nBtZ1q5IBfAB4C4E+FfqLgAFCLc/GMIUolvHVkd78uQmvmIFzx7Z0uehZQYCnBCum8YEnhfB66D/chCtQ00P0u7B/TwbmzErAF1vMeEm1eCGblpWmghlM3v7VIAMmTmIdf+Ri6eIkWC16pKVEYfZME34+O0E2YuJ/u9F8KIuJ+Fm/JkXOk96n69UMJHEXfmt7F4YYXtEsE4aaHzP8IosWjFLk2UTQK7+5ukFvIZ57ipA6OlrRGAwXHo5b7bnUU4z62kxFbsWSJL+5ugHN/uRRh6JJjS+3muUerwu7d43Fh++PQFlJKnq6af1pkv9iMAUV2y1DBAezcF6C3MO+hTRjedZ4SeLSMoc0cKPpgPK11dj4SWqgh8GMfM+STigD2tvddGBiDWofOEDHJfYNqIfNNljYR0gDKenGYTqJwYLB7PzGhm2fW9F2KkeqVTUJMijY8bVVaSAVuHHuZA6mTxVhitfBKAxDgVNAfZ0DFd/ZJCPRqMPNa3lUS4dvsAnpbXh90Oxlpexw0DH3JV+fhaddBaiuyEDd3kwc+MmB6ko7ZkyL978JwzJGj66/nENNyODjj0Z6mQFntxtuoJcK2PZiyb4iXLkwSTrBAbGwoGcl74wfjidse7K7ifXTTnr1rAi2dP1lykuxuq56XOAtyH3OzJGqYqFwOY0Y6KNJStu2GLWkR+PLCCm0gsD/cvXSe7IJXXLs6nbYY4YIqaHVhqGq3EZ9ZECTu3M9Dwkj+POUCyf8ISYmRl1sOZaNnkd0XdCtePn3XCQnRSMubhjiRd0Q2LhBz2NflR1eWuIXjwvRdm4CLJaoG6SXLMsqI5LYkpam71y9PA0bN6Sj/HsHTjRPRE11Fup+CLCvKhMtxyeisjwbWzdbUbLWDJst2kP93xICEwsZHMcd76Dl6u7Kx6NuJ5oOZoHnOcWyGI0RON2SA88DJx525uP+n/lIGR3RzvrfGFqtZqUocI0mE99gErkGszmygePCjlHKZ3A7Vi+PszyrE0W+keO0n7H+t4kS4lciXvr3xtBo/gE4ldbcQK6WtAAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    geometry=None
    def RunScript(self, siteNumber, layer, path, read):
        if path!=None and read==True and layer!=None:
            try:
                if siteNumber!=None:
                    filepath = os.path.join(path,str(int(siteNumber))+layer)
                else:
                    filepath = os.path.join(path,layer)
                f=open(filepath,'rb')
                geometry = pickle.load(f)
                if len(geometry)>0:
                    print "file loaded successfully."
                    self.AddRuntimeMessage(RML.Remark,"file loaded successfully.")
                else:
                    print "the file is empty."
                    self.AddRuntimeMessage(RML.Error,"the file is empty.")
                f.close()

            except:
                print 'problem loading\n %s\nfile may not exist or the path may be invalid.' % filepath
                self.AddRuntimeMessage(RML.Warning,'problem loading\n %s\nfile may not exist or the path may be invalid.' % filepath)
        else:
            if path==None:
                geometry = "please provide path to source directory."
                self.AddRuntimeMessage(RML.Warning,"please provide path to source directory.")
            if layer==None:
                geometry = "please provide layer name of source file."
                self.AddRuntimeMessage(RML.Warning, "please provide layer name of source file.")
            if read!=True:
                geometry = "set read to True to load file contents."
                self.AddRuntimeMessage(RML.Warning, "set read to True to load file contents.")
        return geometry


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "UnPickleData"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("de56e969-a57c-4863-917c-548a14d495ab")