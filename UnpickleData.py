"""
Deserializes data from binary file

Inputs:
	siteNumber: site number
	layer: layer name
	path: path to source file directory.
	read: boolean

Outputs:
	geometry: converted geometry

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
        f=open(filepath,'rb')
        geometry = pickle.load(f)
        if len(geometry)>0:
            print "file loaded successfully."
        else:
            print "the file is empty."
        f.close()

    except:
        print 'problem loading\n %s\nfile may not exist or the path may be invalid.' % filepath
else:
    if path==None:
        print "please provide path to source directory."
    if layer==None:
        print "please provide layer name of source file."
    if read!=True:
        print "set read to True to load file contents."
    else:
        print "Something went wrong. Check your inputs."
        
