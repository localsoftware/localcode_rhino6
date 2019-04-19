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

Author:
	Jaclyn Berry - 19.04.2019
"""
import rhinoscriptsyntax as rs
import scriptcontext as sc
import cPickle as pickle
import Rhino, os

if path!=None and len(data)>0 and layer!=None and write==True:
    try:
        if siteNumber!=None:
            filename = os.path.join(path,str(int(siteNumber))+layer)
        else:
            filename = os.path.join(path,layer)
    
        f = open(filename, 'wb')
        pickle.dump(data, f, -1)
            
        f.close()
        fcheck = open(filename,'rb')
        geometry = pickle.load(fcheck)
        if len(geometry)>0:
            print "file pickled successfully."
        else:
            print "the file didn't save correctly, check your input data."
        fcheck.close()
    except:
        print "There was a problem saving the file. \nThe path your provided may be invalid."

else:
    if not len(data)>0:
        print "please add data or geometry you want to pickle."
    if layer==None:
        print "please provide target file layer name."
    if path==None:
        print "please provide target directory for pickle file."
    if write!=True:
        print "set write to True to save the file."
    else:
        print "something else went wrong, please check your inputs."