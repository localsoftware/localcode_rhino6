rs
import scriptcontext as sc
import Rhino, os, math
import cPickle as pickle
rcdoc = Rhino.RhinoDoc.ActiveDoc

"""
First create view components
"""
if geometry and azimuth and altitude:
    #given geometry get centroid (bounding box)
    bbox = rs.BoundingBox(geometry)
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
    
    #view outputs
    geometry = geometry
    view_target = target
    view_vector = rs.VectorCreate(centroid, cam_pos)
    
elif geometry == None:
    print "input geometry from rhino model"
elif azimuth == None:
    print "input azimuth angle between 0 and 360"
elif altitude == None:
    print "input altitude angle between -90 and 90"


"""
Then pickle view
"""
if geometry and centroid and cam_pos:
    if target_path and layer and write:
        if site_num:
            filename = target_path+str(int(site_num))+layer
        else:
            filename = target_path+layer
    
        f = open(filename, 'wb')
        vec = [centroid[i]-cam_pos[i] for i in range(3)]
        new_data = [geometry,vec,centroid]
        pickle.dump(new_data, f)
        f.close()
        fcheck = open(filename)
        if fcheck:
            print("view pickled successfully")
            fcheck.close()
    elif not target_path:
        print "please provide path to target directory"
    elif not layer:
        print "please provide file layer name"
    elif not write:
        print "Toggle boolean to True to pickle view."
