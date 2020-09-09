from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython, System, Rhino, os
import rhinoscriptsyntax as rs
import scriptcontext as sc
import cPickle as pickle
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "PickleData", "PickleData", """Serializes Rhino data into a binary file.
Exports geometry into Python pickles that can be imported again later.
Pickles are a faster, lighter, and more efficient way to manage files than Rhino files.
Geometry is serialized into pickles, which is a Python binary file.
Based on the work of Jackie Berry.
    Typical usage:
Plug in the geometry you want to export into the data input of the component.
The geometry should be flattened. Plug in a slider or number to the siteNumber input of the component.
Pickle’s numbers always need to start with number one. This will name the pickle according to a specific site.
If you’re only working with one site, you can leave the siteNumber empty. Use a panel to type a layer name for the geometry you are exporting.
Plug the panel into the layer input of the component. Specify a path for the pickles. This will be the folder where the pickles will be exported to.
Finally plug a boolean toggle component to the write input of the component and set it to 'True'.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("42c05bad-2191-4053-a42c-0973b8b5b300")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "data", "data", "geometry or data to serialize")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "siteNumber", "siteNumber", "local code site number (optional)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "layer", "layer", "name of file")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "path", "path", "path of directory for target binary file.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "write", "write", "Script input write.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "geometry", "geometry", "a data tree with serialized geometry")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        result = self.RunScript(p0, p1, p2, p3, p4)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAAMYSURBVEhL3ZVtSFNhFMfn1OUuDpVm0znRnCYtzZla2tamToXqm0SEkUFIZkpRlEkvUEFvUCgpGBYhLAxLsS8VhEhQUd8DCwJfRmKR0Xybqdm/89xtOq/PVfvQlw78GHvOOf8/957nea7ivwylIATfNiZqOpMSNR2rwZik6TAYhE7q3eOVWCHytgk/RkftGB22YnRoFbjteNuzBdR6zasgH8YwVfDdrTkRU1WVBlRVxM1TQ/+PV8lQE49D5XqkJAufSOMUESyqSSLLbl070vs+DzPjdrg/WxYYsuBrnxWuDxa4PnKg9RGXFdMT+eh4mAGdNqyb9ASvrDcizBkal8edD4Dw7FgMClF/YyNiY9SysDyrAxx49zIH4YKq3afNIujKm+4sShYAYyQ4LoEaL9Qls3csC8uLBmJ9Ea5fTmHruwmFUFQQNSwmJyTCfih36bzYIAvLzxtM2+AZsSExXt1DOUX21YsB7jz+1sDXU16mH6ecwtHcsLLBuVojV9gPz6CmMm6WcoqCplvGxUk2B3G4NBO2jmJ0tWciMlLFFWfwDI4e0U1TTmLAxGftwFQ+Wls2YW9pDHYWR+PM6SQ87crCgX16rsHZWslbkDWgAY3RgBz52iUi66LXoKvNjBPHEpCdGb6IliYTMEdPvKwB20X0e7Asbom4n9BQJQZ686iOxKbpSf14bAvisga/7BikZqVSyRX3U1URT/UOYJKE/Ei3ONeATvHzLjNXNBBLbhTwm55A7tww5AxevxBvxWUpcWjJwPdKeeIMrsFPGya/28S7JVBQSuPNVKoPGCiPAIPC5gbfHmZblBrbWtO4wowscyQ89K3AlGSoUkiv+rBBPGimupPraaGE9j81zVAzDbD9wWZsSAkn0SBRWFCHYD+dAbaF53cQq+UxR9DhLN2lG2MGSoM+7NmTRxkYGtiObwO5IjNuK/p7c/HYmYb7zSa8otlMjtDX6wvV9HtruAzmwdVnQUujia7s0HpmwIJ9HKrpKrin1YY4/STEq5zpJrXTnK52pqaonLG6hZw8KqdGo7pDeuWi8r8NheIPyMfxrkDZ9l8AAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))


    def RunScript(self, data, siteNumber, layer, path, write):
        geometry = None
        if path!=None and len(data)>0 and layer!=None and write==True:
            try:
                if siteNumber!=None:
                    filename = os.path.join(path,str(int(siteNumber))+layer)
                else:
                    filename = os.path.join(path,layer)

                f = open(filename, 'wb')
                pickle.dump(data, f, -1)

                f.close()
                fcheck = open(filename,'rb')
                geometry = pickle.load(fcheck)
                if len(geometry)>0:
                    print "file pickled successfully."
                    self.AddRuntimeMessage(RML.Remark,"file pickled successfully.")
                else:
                    print "the file didn't save correctly, check your input data."
                    self.AddRuntimeMessage(RML.Error,"the file didn't save correctly, check your input data.")
                fcheck.close()
            except:
                print "There was a problem saving the file. \nThe path your provided may be invalid."
                self.AddRuntimeMessage(RML.Error,"There was a problem saving the file. \nThe path your provided may be invalid.")

        else:
            if not len(data)>0:
                geometry = "please add data or geometry you want to pickle."
                self.AddRuntimeMessage(RML.Warning,"please add data or geometry you want to pickle.")
            if layer==None:
                geometry = "please provide target file layer name."
                self.AddRuntimeMessage(RML.Warning, "please provide target file layer name.")
            if path==None:
                geometry = "please provide target directory for pickle file."
                self.AddRuntimeMessage(RML.Warning, "please provide target directory for pickle file.")
            if write!=True:
                geometry = "set write to True to save the file."
                self.AddRuntimeMessage(RML.Warning, "set write to True to save the file.")
            else:
                geometry = "something else went wrong, please check your inputs."
                self.AddRuntimeMessage(RML.Error, "something else went wrong, please check your inputs.")

        # return outputs if you have them; here I try it for you:
        return geometry


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "PickleData"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("c82f13fc-b368-4b8d-b3ed-73240c5dfbff")