"""Creates view target and vector from seleted objects.
    Inputs:
        geometry: geometry to focus on in view
        azimuth: Camera rotation in XY. 0 to 360.
        altitiude: Camera z-position. -90 to 90.
    Output:
        out: status text
        geometry:
        view_target:
        view_vector:"""

__author__ = "jberry"
__version__ = "2019.04.10"

import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino, os, math
rcdoc = Rhino.RhinoDoc.ActiveDoc

if geometry and azimuth and altitude:
    #given geometry get centroid (bounding box)
    bbox = rs.BoundingBox(geometry)
#    print bbox
    #cam target is centroid
    centroid = [0,0,0]
    for pt in bbox:
        centroid = [centroid[0]+pt[0]/8, centroid[1]+pt[1]/8, centroid[2]+pt[2]/8]
    
    target = rs.AddPoint(centroid)
    view_dist = rs.Distance(bbox[0], bbox[6])
    
#    print view_dist

    # convert angles to radians
    azimuth = azimuth*2*math.pi/360 
    altitude = altitude*2*math.pi/360
    X = centroid[0] + view_dist*math.cos(azimuth)
    Y = centroid[1] + view_dist*math.sin(azimuth)
    Z = centroid[2] + view_dist*math.sin(altitude)
    cam_pos = [X, Y, Z]
    
    geometry = geometry
    view_target = target
    view_vector = rs.VectorCreate(centroid, cam_pos)
    
elif geometry == None:
    print "input geometry from rhino model"
elif azimuth == None:
    print "input azimuth angle between 0 and 360"
elif altitude == None:
    print "input altitude angle between -90 and 90"
