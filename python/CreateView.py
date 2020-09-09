"""Creates view target and vector from seleted objects.

Transforms view data into a Rhino view.
Creating a view is the first step to set a view in Rhino’s viewport.
To select a view, you need a geometry to point to. You can define view angles.
Based on the work of Jackie Berry.

    Typical usage:
        Input the curve to point to, so you should never input a surface, brep or mesh as geometry to create a view.
        Select an Azimuth and Altitude angle. The angles go between 0 and 360, and represent the position of a “camera” around the base object.

    Inputs:
        geometry: curve geometry to focus on in view
        azimuth: Camera rotation in XY. 0 to 360.
        altitude: Camera z-position. -90 to 90.

    Output:
        view_geom: geometry in view
        view_target: 3D point for camera target.
        view_vector: 3D vector defining camera direction."""

__author__ = "palomagr"
__version__ = "2020.07.09"

#ghenv.Component.Name = "Create View"
#ghenv.Component.NickName = "Create View"


from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino, os, math
import rhinoscriptsyntax as rs
import scriptcontext as sc

rcdoc = Rhino.RhinoDoc.ActiveDoc
ghdoc = sc.doc

class MyComponent(component):
    view_geom, view_target, view_vector = None, None, None

    def RunScript(self, geometry, azimuth, altitude):
        view_geom, view_target, view_vector = None, None, None
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
