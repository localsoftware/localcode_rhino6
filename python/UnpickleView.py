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
"""
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino, os
import rhinoscriptsyntax as rs
import cPickle as pickle

class MyComponent(component):
    geometry, vector, target, status  = None, None, None, None
    
    def RunScript(self, siteNumber, layer, path, read):
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
                    status = "file successfully loaded"
                else:
                    status = "This doesn't look like a view file. \nTry the UnpickleData component instead."
                f.close()
        
            except:
                status = 'Problem loading\n\n %s\n\nFile may not exist or the path may be invalid' % filepath
        else:
            geometry, vector, target  = None, None, None
            if path==None:
                status = "please provide path to source file directory."
            if layer==None:
                status = "please provide layer name of source file."
            if read!=True:
                status = "set read to True to unpickle view file."
        
        # return outputs if you have them; here I try it for you:
        return (geometry, vector, target, status)
