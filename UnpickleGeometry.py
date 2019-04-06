"""
Deserializes data from binary file

Inputs:
	siteNumber: site number
	layer: layer name
	path: path to source file directory.
	read: boolean

Outputs:
	geometry: converted geometry
"""

import cPickle as pickle

if path and read and layer:
    try:
        if siteNumber:
            f = open(path+str(int(siteNumber))+layer)
        else:
            f = open(path+layer)
        geometry = pickle.load(f)
        f.close()

    except:
        print 'problem loading %s\nfile may not exist' % path+str(int(siteNumber))+layer
        
