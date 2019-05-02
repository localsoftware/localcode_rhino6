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

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino, os
import rhinoscriptsyntax as rs
import cPickle as pickle

__author__ = "jberry"
__version__ = "2019.05.02"

class MyComponent(component):
    
    def RunScript(self, siteNumber, layer, path, read):
        print read
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
                geometry = "please provide path to source directory."
            if layer==None:
                geometry = "please provide layer name of source file."
            if read!=True:
                geometry = "set read to True to load file contents."
            else:
                geometry = "Something went wrong. Check your inputs."
        return geometry
