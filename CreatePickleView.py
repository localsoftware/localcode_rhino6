"""
Serializes Rhino view data into binary file.

Inputs:
    data: geometry or data to serialize
    azimuth: rotation in XY of camera angle.
    altidue: vertical rotation of camera angle.
    siteNumber: local code site number (sort of optional)
    path: path of directory for target binary file.
    layer: name of file
    write: boolean

Outputs:
    geometry: if successful, a data tree with serialized geometry
    view_vector: a vector specifying the camera angle
    view_target: a 3D point specifying the camera target (center of geom bbox)
	
Author:
	Jaclyn Berry - 19.04.2019
"""
import rhinoscriptsyntax as rs
import scriptcontext as sc
import cPickle as pickle
import Rhino, math, os

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
            print "View and geometry pickled successfully."
        else:
            print "It looks like the file didn't save correctly. \nTry the pickleData and UnpickleData components to debug."
        fcheck.close()
    except:
        print "Unable to pickle the view file. \nThe path your provided may be invalid."
else:
    if not len(data)>0:
        print "specify objects (data) in view to pickle."
    if azimuth==None:
        print "specify view angle azimuth."
    if altitude==None:
        print "specify view angle altitude."
    if layer==None:
        print "specify file layer name."
    if path==None:
        print "specify path to target directory"
    if write!=True:
        print "set write to True to pickle view"
    else:
        print "Something went wrong. Please check your inputs."