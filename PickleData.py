"""
Serializes Rhino data into binary file.

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
import Rhino

if path!=None and len(data)>0 and write!=False:
    if siteNumber!=None:
        filename = path+str(int(siteNumber))+layer
    else:
        filename = path+layer

    f = open(filename, 'wb')
    pickle.dump(data, f, -1)
        
    f.close()
    fcheck = open(filename)
    geometry = pickle.load(fcheck)
    fcheck.close()