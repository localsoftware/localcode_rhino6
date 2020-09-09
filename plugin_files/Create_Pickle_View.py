from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython, System, Rhino, os, math
import rhinoscriptsyntax as rs
import scriptcontext as sc
import cPickle as pickle
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML


class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "CreatePickleView", "CreatePickleView", """Serializes Rhino view data into a binary file.
Returns a pickled file with view information to be set up in Rhino.
Based on the work of Jackie Berry.
    Typical usage:
Input a geometry (make sure to only input one geometry), and Azimuth and Altitude angles for the view.
Set a path with a panel to export the Pickled View to. Finally use a Boolean Toggle to activate the component.
You can use the component’s outputs to set a view and visualize the results of the parameters used to create the view.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("7604b8c9-36bf-4577-a712-6a8f3da4bc86")
    
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
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "azimuth", "azimuth", "rotation in XY of camera angle.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "altitude", "altitude", "vertical rotation of camera angle.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "siteNumber", "siteNumber", "local code site number (sort of optional)")
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
        self.SetUpParam(p, "write", "write", "boolean")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "geometry", "geometry", "if successful, a data tree with serialized geometry")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "view_vector", "view_vector", "a vector specifying the camera angle")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "view_target", "view_target", "a 3D point specifying the camera target (center of geom bbox)")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "status", "status", "Script variable CreatePickleView")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        p5 = self.marshal.GetInput(DA, 5)
        p6 = self.marshal.GetInput(DA, 6)
        result = self.RunScript(p0, p1, p2, p3, p4, p5, p6)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
                self.marshal.SetOutput(result[3], DA, 3, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAAPnSURBVEhL3VVpaFNZFH5pTF986SRtYjutGmKqrY00RsclW7OYqLgLIqKIC1W0KkVc60LBP27gTGcYyQ+RgUHQqvjDhSr+UBBR6gLuG9Zaly5irbY2Vrt8nvteXtI0LRVk/syBj7x37/m+c94959xw/08TBOWfOTma0zkjfhDkazZpThN1qaTQj9nH62qbmwL4VOfFp9r+0fzBjzvXnOA4xcGIRJ9mVicrD7mc2nDRKiOKVgztG4VDUVxkxI4tw7BxvQnLFw9Gbm5KDWmUEtSiWg+z+R36dw/vOdHRSlnVOXtFC+HbBzfQ7kP1Ewc2FZtw5rgV4c8e4vlQcWYsjEbhOumlSrKSpVgsmqqWRh8AP9DqAcLeRIDtB9FY60HpjuEI+tNRuMyIuTMzgY5JQBvzCeD+TTv0Or4ioi1a6aVzY2mTnJpJvKUHIsLVT10o2WzGIAOPnVuy0d5G/piKieP0OH/KRs+UHOOTb6gsj2rCLWTivMetf4lOcmaZM0GWyTeWDREoo3u37Fi90giNoGIkEaEyC06U22DL14rvs6dniL6go2L89hYf8kZqKlmA/NKSbGlTjD4Jre88aKgpwPUrE7BgfhaUSUlR4b6gUCThwY2JQGfsK4pWZH2lPc5Vtj9PCkDi5UesGJGdgrQ0NREVUYFUbTIO/mXBwzt2nCwfTT6a6J6M5YuHiMLSsQawfXM2W+ccB/aMpIXJqHrsxEB17BhkqFRKXLs8njongBNH8tHwtgANb7zIymRJxPx4Xoka0kAHq1kAWzeYu2hdDhDE+zcF+DUjnsQQ8Btofwo8Lr34rk/l0UUF3r5pWILvhnUmUbyXANLigd25CaQ5M1kBp8BkFKJrX5q82LtreJyfhCTUV9Oc0IkkBvjqxce6AujT+DiSTqtCPRX92SMH1tAUXzg7ho5hMqyRDpJhs+oQ+tuCz41SkRMDiMUJ0qeb44gMrB1vV9qpfYN49cKN2dPSo3setwEnj45GZ1hqa7Hd6bf3AHQF1D53QRg4IC6ADC11k/w8a0YGLlb8Jk0xG9Iw8ZlGpIt6DxD5itWFxjjhGBRYtGAwKq9OkDjy1SJzoxrdAvy+t0eATh+eUb8rlbEBY5kXrzXh8V1HTJhNbXfR7iCfko1SAOcf+3oEYER6nzc3EwY9L15sr6tYZ9AQdVGPdxfqC8TfJtWSM6+ju59dWuiI3EEMJNRc58bHt1LLiRnLe/2BToC19cL56W0sAJeRzh8/9q8VNVTc+heEKgI9N712o4mGjz2Laz8C6rBq8j8cGgXdL6qQGIBMRVgpCMkhg0H9jyHtJ0B8QVCxv84lBAUT/w+N474Dx530k5e70fcAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))


    def RunScript(self, data, azimuth, altitude, siteNumber, layer, path, Write):
        geometry, view_vector, view_target, status = None, None, None, None
        if data ==None:
            self.AddRuntimeMessage(RML.Warning,"Add data as input.")
        if path ==None:
            self.AddRuntimeMessage(RML.Warning,"Add a path.")
        if Write == None:
            self.AddRuntimeMessage(RML.Warning,"Add a boolean toggle in the 'Write' input.")
            
            
        if path!=None and len(data)>0 and write==True and azimuth!=None and altitude!=None:
            bbox = rs.BoundingBox(data)
            centroid = [0,0,0]
            for pt in bbox:
                centroid = [centroid[0]+pt[0]/8, centroid[1]+pt[1]/8, centroid[2]+pt[2]/8]
            target = rs.AddPoint(centroid)
            target = rs.coerce3dpoint(target)

            # convert angles to radians
            azimuth = azimuth*2*math.pi/360
            altitude = altitude*2*math.pi/360
            X = centroid[0] + math.cos(azimuth)
            Y = centroid[1] + math.sin(azimuth)
            Z = centroid[2] + math.sin(altitude)
            cam_pos = [X, Y, Z]

            vector = rs.VectorCreate(centroid, cam_pos)
            vector = rs.coerce3dvector(vector)

            try:
                if siteNumber!=None:
                    filename = os.path.join(path,str(int(siteNumber))+layer)
                else:
                    filename = os.path.join(path,layer)

                outdata=[]
                outdata+=data
                outdata+=[target]
                outdata+=[vector]

                f = open(filename, 'wb')
                pickle.dump(outdata, f, -1)

                f.close()
                fcheck = open(filename,'rb')
                checkdata = pickle.load(fcheck)
                if len(checkdata)>2:
                    geometry=checkdata[:-2]
                    view_target=checkdata[-2]
                    view_vector=checkdata[-1]
                    status = "View and geometry pickled successfully."
                else:
                    status = "It looks like the file didn't save correctly. \nTry the pickleData and UnpickleData components to debug."
                fcheck.close()
            except:
                status = "Unable to pickle the view file. \nThe path your provided may be invalid."
        else:
            if not len(data)>0:
                status = "specify objects (data) in view to pickle."
            if azimuth==None:
                status = "specify view angle azimuth."
            if altitude==None:
                status = "specify view angle altitude."
            if layer==None:
                status = "specify file layer name."
            if path==None:
                status = "specify path to target directory"
            if Write!=True:
                status = "set write to True to pickle view"

        # return outputs
        return (geometry, view_vector, view_target, status)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "CreatePickleView"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("ecc81d21-8891-4a63-871b-d9ccbc9558f5")