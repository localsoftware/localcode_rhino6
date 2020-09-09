"""Serializes Rhino view data into a binary file.

Returns a pickled file with view information to be set up in Rhino.
Based on the work of Jackie Berry.

    Typical usage:
        Input a geometry (make sure to only input one geometry), and Azimuth and Altitude angles for the view.
        Set a path with a panel to export the Pickled View to. Finally use a Boolean Toggle to activate the component.
        You can use the component’s outputs to set a view and visualize the results of the parameters used to create the view.


    Inputs:
        data: geometry or data to serialize
        azimuth: rotation in XY of camera angle.
        altitude: vertical rotation of camera angle.
        siteNumber: local code site number (sort of optional)
        path: path of directory for target binary file.
        layer: name of file
        write: boolean

    Outputs:
        geometry: if successful, a data tree with serialized geometry
        view_vector: a vector specifying the camera angle
        view_target: a 3D point specifying the camera target (center of geom bbox)"""

__author__ = "palomagr"
__version__ = "2020.07.09"

#ghenv.Component.Name = "Create Pickle View"
#ghenv.Component.NickName = "Create Pickle View"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino, os, math
import rhinoscriptsyntax as rs
import scriptcontext as sc
import cPickle as pickle

class MyComponent(component):

    def RunScript(self, data, azimuth, altitude, siteNumber, layer, path, write):
        geometry, view_vector, view_target, status = None, None, None, None

        if path!=None and len(data)>0 and write==True and azimuth!=None and altitude!=None:
            bbox = rs.BoundingBox(data)
            centroid = [0,0,0]
            for pt in bbox:
                centroid = [centroid[0]+pt[0]/8, centroid[1]+pt[1]/8, centroid[2]+pt[2]/8]
            target = rs.AddPoint(centroid)
            target = rs.coerce3dpoint(target)

            # convert angles to radians
            azimuth = azimuth*2*math.pi/360
            altitude = altitude*2*math.pi/360
            X = centroid[0] + math.cos(azimuth)
            Y = centroid[1] + math.sin(azimuth)
            Z = centroid[2] + math.sin(altitude)
            cam_pos = [X, Y, Z]

            vector = rs.VectorCreate(centroid, cam_pos)
            vector = rs.coerce3dvector(vector)

            try:
                if siteNumber!=None:
                    filename = os.path.join(path,str(int(siteNumber))+layer)
                else:
                    filename = os.path.join(path,layer)

                outdata=[]
                outdata+=data
                outdata+=[target]
                outdata+=[vector]

                f = open(filename, 'wb')
                pickle.dump(outdata, f, -1)

                f.close()
                fcheck = open(filename,'rb')
                checkdata = pickle.load(fcheck)
                if len(checkdata)>2:
                    geometry=checkdata[:-2]
                    view_target=checkdata[-2]
                    view_vector=checkdata[-1]
                    status = "View and geometry pickled successfully."
                else:
                    status = "It looks like the file didn't save correctly. \nTry the pickleData and UnpickleData components to debug."
                fcheck.close()
            except:
                status = "Unable to pickle the view file. \nThe path your provided may be invalid."
        else:
            if not len(data)>0:
                status = "specify objects (data) in view to pickle."
            if azimuth==None:
                status = "specify view angle azimuth."
            if altitude==None:
                status = "specify view angle altitude."
            if layer==None:
                status = "specify file layer name."
            if path==None:
                status = "specify path to target directory"
            if write!=True:
                status = "set write to True to pickle view"

        # return outputs
        return (geometry, view_vector, view_target, status)
