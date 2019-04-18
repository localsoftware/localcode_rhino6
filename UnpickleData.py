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

if path!=None and read!=False and layer!=None:
    try:
        print siteNumber
        if siteNumber!=None:
            f = open(path+str(int(siteNumber))+layer)
        else:
            f = open(path+layer)
        geometry = pickle.load(f)
        f.close()

    except:
        print 'problem loading %s\nfile may not exist' % path+str(int(siteNumber))+layer
        
