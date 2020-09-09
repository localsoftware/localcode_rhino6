from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython, System, Rhino, os, math
import rhinoscriptsyntax as rs
import scriptcontext as sc
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

rcdoc = Rhino.RhinoDoc.ActiveDoc
ghdoc = sc.doc

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "CreateView", "CreateView", """Creates view target and vector from seleted objects.
Transforms view data into a Rhino view.
Creating a view is the first step to set a view in Rhino’s viewport.
To select a view, you need a geometry to point to. You can define view angles.
Based on the work of Jackie Berry.
    Typical usage:
Input the curve to point to, so you should never input a surface, brep or mesh as geometry to create a view.
Select an Azimuth and Altitude angle. The angles go between 0 and 360, and represent the position of a “camera” around the base object.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("b1996ce9-0a0d-4bcd-b147-145bcd380adb")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "geometry", "geometry", "curve geometry to focus on in view")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "azimuth", "azimuth", "Camera rotation in XY. 0 to 360.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Number()
        self.SetUpParam(p, "altitude", "altitude", "Camera z-position. -90 to 90.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "view_geom", "view_geom", "geometry in view")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "view_target", "view_target", "3D point for camera target.")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "view_vector", "view_vector", "3D vector defining camera direction.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
                self.marshal.SetOutput(result[2], DA, 2, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAANMSURBVEhLxZVbSJRREMe/Nde77q5kmrfAS1iuia578barqxLYQwgGESFiYBRIF6gkKSqKonoT6kUMukhpBCUuVNiDkRIJJollJkahEEFlfnnJzek/53NdzQubFf3hhzPzzZk5Z85hlf63VoN0xRSKBbdAlvAUJQOOr0inAAFf4UlSDGB/s/AU9QGHYnqmcBCimKLgOHCdghu9BEnCk6RgIIN84UnSKsDrl5Q/GACNwlNUC/YrptANEKGYUiFoVkwhzhsBkcJbRF5gK3CCYg5AcaBGMYX2giDFlCqBXTHFPfA6zvXhwHLiS7wP1ghPkkzAtSgR8ChUwAx4U2pwHewGHot3zrvjQiwuNFeuOMsIeFweKWwGvsAADvwt8Y7KwBfAF8XUAX4VfKnLwaP8NbbgHi4lb9B8N2aEkjFd5yZDM2rO0MhLYtDIudk6Oc+qlW05GjnPppVzMnWyWq1qRU33WFUqr7bBniwiKiCazF/IFOBvVAQKiZwzccQe3jPQ+dMmqr2YSRfOmqm5KY2Sknw/oKz7FCqV6kF/txkLbETfct3IYBqx6Xzq7jDS3Zsp1PHIQDSGGOWJ/OPVCVS2o5iOVZdSRdkWOnIwHqcPeIuy8xv0daHBDywcRVHmK3DaaGgwm4oKwvgnYpYUfQh1tpvQwE49T9Op8WoyNV1LpsYGPXW2pVFior8HDcatNDZio016jSi6c3sk1dfp6UDVOuHrtL707jWPlUfFp2Fg49TR0d4eNEDylcsbRbGjh+Lg8/zt4m9DvV7E9+2JVWKuNRNWGv+Y7WkDO2a7VhQa7sdO+S5mitC4jbQaH5wuGGuUXa+oQWVFlGjQ322BjxHwvUxZyTlipcBAbzIZtH/SIJ9abqeKBqUlEeSc5PHwUy2gmsNxIn7uRILYyOya32rAzxTvf1uJMqb18UFUXh5DZqNW+GmpGhr9hHHxyDxp8P5Vpti18u4BNxMvw05nsNPoKD9ROFSnpipc7gRemMjnPNcazsfGYhY28Gp33Emn3p5M6u20uHlmpr7nFhoeyKHOxxbinPZWEw3159CbF8jF93n5yO16YqLwcJ/PKOtuAO1CmxaA/6+Lo1Z7O4IC1Q4/X+9Fv89HOgnm/qT/C0nSTw0bl6OgcEo6AAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    view_geom, view_target, view_vector = None, None, None

    def RunScript(self, geometry, azimuth, altitude):
        view_geom, view_target, view_vector = None, None, None
        if geometry == None:
            self.AddRuntimeMessage(RML.Warning,"add geometry")
        if azimuth == None:
            self.AddRuntimeMessage(RML.Warning,"add azimuth")
        if altitude == None:
            self.AddRuntimeMessage(RML.Warning,"add altitude")
        if geometry!=None and azimuth!=None and altitude!=None:
            #given geometry get centroid (bounding box)
            bbox = rs.BoundingBox(geometry)
            #cam target is centroid
            centroid = [0,0,0]
            for pt in bbox:
                centroid = [centroid[0]+pt[0]/8, centroid[1]+pt[1]/8, centroid[2]+pt[2]/8]

            target = rs.AddPoint(centroid)
            view_dist = rs.Distance(bbox[0], bbox[6])

            # convert angles to radians
            azimuth = azimuth*2*math.pi/360
            altitude = altitude*2*math.pi/360
            X = centroid[0] + view_dist*math.cos(azimuth)
            Y = centroid[1] + view_dist*math.sin(azimuth)
            Z = centroid[2] + view_dist*math.sin(altitude)
            cam_pos = [X, Y, Z]

            view_geom = geometry
            view_target = target
            view_vector = rs.VectorCreate(centroid, cam_pos)

        # return outputs if you have them; here I try it for you:
        return (view_geom, view_target, view_vector)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "CreateView"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("ce9ecb28-2824-4226-90c2-11a6b672d5f1")