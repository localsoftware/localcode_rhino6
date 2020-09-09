"""Serializes Rhino data into a binary file.

Exports geometry into Python pickles that can be imported again later.
Pickles are a faster, lighter, and more efficient way to manage files than Rhino files.
Geometry is serialized into pickles, which is a Python binary file.
Based on the work of Jackie Berry.

    Typical usage:
        Plug in the geometry you want to export into the data input of the component.
        The geometry should be flattened. Plug in a slider or number to the siteNumber input of the component.
        Pickle’s numbers always need to start with number one. This will name the pickle according to a specific site.
        If you’re only working with one site, you can leave the siteNumber empty. Use a panel to type a layer name for the geometry you are exporting.
        Plug the panel into the layer input of the component. Specify a path for the pickles. This will be the folder where the pickles will be exported to.
        Finally plug a boolean toggle component to the write input of the component and set it to 'True'.


    Inputs:
        data: geometry or data to serialize
        siteNumber: local code site number (optional)
        path: path of directory for target binary file.
        layer: name of file
        Write: boolean

    Outputs:
        geometry: a data tree with serialized geometry"""

__author__ = "palomagr"
__version__ = "2020.07.09"

#ghenv.Component.Name = "Pickle Data"
#ghenv.Component.NickName = "Pickle Data"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino, os
import rhinoscriptsyntax as rs
import scriptcontext as sc
import cPickle as pickle

class MyComponent(component):

    def RunScript(self, data, siteNumber, layer, path, write):
        geometry = None
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
                geometry = "please add data or geometry you want to pickle."
            if layer==None:
                geometry = "please provide target file layer name."
            if path==None:
                geometry = "please provide target directory for pickle file."
            if write!=True:
                geometry = "set write to True to save the file."
            else:
                geometry = "something else went wrong, please check your inputs."

        # return outputs if you have them; here I try it for you:
        return geometry
