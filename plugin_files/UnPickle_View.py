from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython, System, Rhino, os
import rhinoscriptsyntax as rs
import cPickle as pickle
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML


class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "UnPickleView", "UnPickleView", """Deserializes view data from binary file.
Sets a view by un-pickling a pickled view file.
Returns a site geometry, a camera vector and a focal point.
Based on the work of Jackie Berry.
    Typical usage:
Plug in a slider or number to the siteNumber input of the component. This numbere will be the site number, and name of the pickle.
If you’re only working with one site, you can leave it empty.
Specify a path for the pickles. This is the folder where the pickles are.
Finally plug in a boolean toggle component to the read input of the component.
Once you are ready to UnPickle the geometry, set it to true.
The component will return a site geometry a camera vector and a camera target.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("0032ef71-cb63-41c1-9449-2ea7bccf3b0e")
    
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
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "vector", "vector", "camera view vector")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "target", "target", "camera view target (3D Point)")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "status", "status", "Script variable UnPickleView")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        result = self.RunScript(p0, p1, p2, p3)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
                self.marshal.SetOutput(result[3], DA, 3, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAAOsSURBVEhL3VRZTFNBFG1faV8XIy3QWgyltNhoVAREFLCLBfftw08//FGjwX0BXNAofqg/+uMSoyEu+AMYN1RiYtS4oEZE3IJGjVFQEXGpgiI0xzvzSqVaBfTPm5y8eXPnnnPn3pmR/TcWSSiMjdWW26y649Z/gM2mO24yiWXEl0fQMHKF2ag+d+poCppfu/CJ4Hv192DxTfQtPZQEfaSqlAkMzp1rATAOaHMDX3uADgI84X0M3wjEN2O62c8E3FuKBtBENvDJ1T1aXGh7R1k+Gy3FtIZZw0C+5YusYALOXgkgB+sK7DAZ1dizczDQ7qW5MWHWdRHYvLGHAn4Pnt7PhEYdwQI53KOjceXiCC6MdiqNL7CW+JYt7I0AlYatmTbJFCT/ATly58Wjsd4p8bCy9UqAZQUvKsqSfyIORWw/Dfbs6ixbDpYu6KkAnYyvPg8SbbpfSMPB645B2+ds5C9LYP89EKBsNqxJ5MEJ8VoU5Ns5rBZtCHFXNL9worDAxsbdCAQaq1QqMGK4Hl98XvhbCK1etH70Ij1N/wt5SlIkvn3JQd7S7nYQaOzUiVJja66m487NUTBEqmDQq3Dv1ihUX04nnzxIPnaMEbXVGRQ3Lthk99ZNYQQCjT1VLjVWLpej44Mb6/N5VhwbVttpzgNBUPB/cz81WpvphlMc41uxWBJIWpIbTxN0jrsKUGPbqLED7H2ChGdPpOBNg4uXgKGJxpXHUoL+kr1DpER5ctmYNbN/O83LlA6H9pG/hW4je0c6BUiwaK3U2E7QS4tH97PIR+8Woe5uJqzUdOZjFw5+ImdlZcnRbu02XQ35uM3bvX0QJ+XkHR7crkrnjSVfCNSqCEyZbMLECUaoAn5BEFB7bSTFU5I8+xwwPvLNIXAT+vZVXqipYotIhLa3d+eQEOI/YeXiBIoZK1WAYh/WZiAmWlVFPgUhaDFmo3i99PAwfHzrRGNDFkr2D+VnXVTJERWlQKxZyWEwRKDsYBLWrbIhOkpEXc1IvHyeAV+TE5UVqVQazQPii5NoQ00k5Fks2vr5s+NQuMbGr/uBfck4czINO7YNxD56QasvsZ2OR/WNTGzZOAgrlidg0XwLHA7xPcUXEfSM7LcmisqKBzez8PaVG+/r6e1vcOPKhQxke8y8JKePpOJ8ZRpSk2Pw/LGLr2t84oQlTqyTGLoxQZDN1evVxQZDADS2WHTFjkRdMbmL1Wqhlt0LjSaixGTScD8DNXu1xPDvpiK4pOGfTCb7Di+eCmvvWxIBAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    geometry, vector, target, status  = None, None, None, None

    def RunScript(self, siteNumber, layer, path, read):
        if path!=None and read==True and layer!=None:
            try:
                if siteNumber!=None:
                    filepath = os.path.join(path,str(int(siteNumber))+layer)
                else:
                    filepath = os.path.join(path,layer)
                f = open(filepath, 'rb')
                data = pickle.load(f)
                if len(data)>2:
                    geometry = data[:-2]
                    vector = data[-1]
                    target = data[-2]
                    status = "file successfully loaded"
                    self.AddRuntimeMessage(RML.Remark,"file successfully loaded")
                else:
                    status = "This doesn't look like a view file. \nTry the UnpickleData component instead."
                    self.AddRuntimeMessage(RML.Remark,"This doesn't look like a view file. \nTry the UnpickleData component instead.")
                f.close()

            except:
                status = 'Problem loading\n\n %s\n\nFile may not exist or the path may be invalid' % filepath
                self.AddRuntimeMessage(RML.Remark,'Problem loading\n\n %s\n\nFile may not exist or the path may be invalid' % filepath)
        else:
            geometry, vector, target  = None, None, None
            if path==None:
                status = "please provide path to source file directory."
                self.AddRuntimeMessage(RML.Warning,"please provide path to source file directory.")
            if layer==None:
                status = "please provide layer name of source file."
                self.AddRuntimeMessage(RML.Warning,"please provide layer name of source file.")
            if read!=True:
                status = "set read to True to unpickle view file."
                self.AddRuntimeMessage(RML.Warning,"set read to True to unpickle view file.")

        # return outputs if you have them; here I try it for you:
        return (geometry, vector, target, status)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "UnPickleView"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("47ed530f-c118-4471-8204-916377aefe3c")