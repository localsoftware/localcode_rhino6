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
        print siteNumber
        if siteNumber!=None:
            f = open(path+str(int(siteNumber))+layer)
        else:
            f = open(path+layer)
        data = pickle.load(f)
        geometry = data[:-2]
        vector = data[-1]
        target = data[-2]
        f.close()

    except:
        print 'problem loading %s\nfile may not exist' % path+str(int(siteNumber))+layer
        
