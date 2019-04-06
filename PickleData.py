'''
Serializes Rhino data into binary file.

Inputs:
	data: geometry or data to serialize
	siteNumber: local code site number (sort of optional)
	path: path of directory for target binary file.
	layer: name of file
	write: boolean
	
Outputs:
	geometry: if successful, a data tree with serialized geometry
	
	
TODO:
Very broken.
Geometry not preserved --> try object.Geometry
Make siteNumber optional
'''

import cPickle as pickle

if path and data and write:
    if siteNumber:
        f = open(path+str(int(siteNumber))+layer, 'wb')
    else:
        f = open(path+layer, 'wb')
        print f
    pickle.dump(data, f)
    f.close()
    fcheck = open(path+str(int(siteNumber))+layer)
    geometry = pickle.load(fcheck)
    fcheck.close()