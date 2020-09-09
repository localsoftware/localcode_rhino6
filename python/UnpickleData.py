"""Deserializes data from binary file.

Un-pickles (de-serializes) pickled files into Grasshopper geometries.
Un-pickling geometry is faster and more efficient than importing Rhino files.
Based on the work of Jackie Berry.

    Typical usage:
        You need to provide a path for the folder that contains the files to be imported.
        Use the string concatenate component to join the file path of the folder with the number of the file to be imported.
        You can specify the file number with a slider. Specify the name of the layers you want to import from the rhino file.
        Type the layer names in a Panel. Make sure the Multiline Data option is unchecked (you can uncheck the box while typing in the panel or by right click).

    Inputs:
        siteNumber: site number
        layer: layer name
        path: path to source file directory.
        read: boolean

    Outputs:
        geometry: converted geometry"""

__author__ = "palomagr"
__version__ = "2020.07.09"

#ghenv.Component.Name = "Unpicke Data"
#ghenv.Component.NickName = "Unpickle Data"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino, os
import rhinoscriptsyntax as rs
import cPickle as pickle

class MyComponent(component):
    geometry=None
    def RunScript(self, siteNumber, layer, path, read):
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
        return geometry
