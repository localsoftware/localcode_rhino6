"""
Deserializes view data from binary file

Inputs:
	siteNumber: site number
	layer: layer name
	path: path to source file directory.
	read: boolean

Outputs:
	geometry: converted geometry
	vector: camera view vector
	target: camera view target (3D Point)
	
Author:
	Jaclyn Berry - 19.04.2019
"""

import cPickle as pickle
import os

if path!=None and read==True and layer!=None:
    try:
        if siteNumber!=None:
            filepath = os.path.join(path,str(int(siteNumber))+layer)
        else:
            filepath = os.path.join(path,layer)
        f = open(filepath, 'rb')
        data = pickle.load(f)
        if len(data)>2:
            geometry = data[:-2]
            vector = data[-1]
            target = data[-2]
            print "file successfully loaded"
        else:
            print "This doesn't look like a view file. \nTry the UnpickleData component instead."
        f.close()

    except:
        print 'Problem loading\n\n %s\n\nFile may not exist or the path may be invalid' % filepath
else:
    if path==None:
        print "please provide path to source file directory."
    if layer==None:
        print "please provide layer name of source file."
    if read!=True:
        print "set read to True to unpickle view file."
    else:
        print "Something went wrong. Please check your inputs."
