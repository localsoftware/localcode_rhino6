"""
Serializes Rhino view data into binary file.

Inputs:
    data: geometry or data to serialize
    siteNumber: local code site number (sort of optional)
    path: path of directory for target binary file.
    layer: name of file
    write: boolean

Outputs:
    geometry: if successful, a data tree with serialized geometry
"""
import rhinoscriptsyntax as rs
import scriptcontext as sc
import cPickle as pickle
import Rhino, math

if path!=None and len(data)>0 and write!=False and azimuth!=None and altitude!=None:
    bbox = rs.BoundingBox(data)
    centroid = [0,0,0]
    for pt in bbox:
        centroid = [centroid[0]+pt[0]/8, centroid[1]+pt[1]/8, centroid[2]+pt[2]/8]
    target = rs.AddPoint(centroid)
    print type(target)
    target = rs.coerce3dpoint(target)
    print type(target)
    
    # convert angles to radians
    azimuth = azimuth*2*math.pi/360 
    altitude = altitude*2*math.pi/360
    X = centroid[0] + math.cos(azimuth)
    Y = centroid[1] + math.sin(azimuth)
    Z = centroid[2] + math.sin(altitude)
    cam_pos = [X, Y, Z]
    
    vector = rs.VectorCreate(centroid, cam_pos)
    vector = rs.coerce3dvector(vector)
    
    if siteNumber!=None:
        filename = path+str(int(siteNumber))+layer
    else:
        filename = path+layer
        
    outdata=[]
    outdata+=data
    outdata+=[target]
    outdata+=[vector]

    f = open(filename, 'wb')
    pickle.dump(outdata, f, -1)
        
    f.close()
    fcheck = open(filename)
    data = pickle.load(fcheck)
    geometry=data[:-2]
    view_target=data[-2]
    view_vector=data[-1]
    fcheck.close()