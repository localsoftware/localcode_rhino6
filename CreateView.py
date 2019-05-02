"""Creates view target and vector from seleted objects.
    Inputs:
        geometry: geometry to focus on in view
        azimuth: Camera rotation in XY. 0 to 360.
        altitiude: Camera z-position. -90 to 90.
    Output:
        
        view_geom: geometry in view
        view_target: 3D point for camera target.
        view_vector: 3D vector defining camera direction.
"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino, os, math
import rhinoscriptsyntax as rs
import scriptcontext as sc

rcdoc = Rhino.RhinoDoc.ActiveDoc
ghdoc = sc.doc

__author__ = "jberry"
__version__ = "2019.04.10"


class MyComponent(component):
    
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
