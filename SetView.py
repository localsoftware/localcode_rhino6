"""Set current viewport to camera view.
    Inputs:
        setView: boolean to set view
        geometry: geometry in view 
        target: 3D point defining camera target
        vector: 3D vector defining camera direction
    Outputs:
        None
"""

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino, os
import rhinoscriptsyntax as rs
import cPickle as pickle
from scriptcontext import doc

class MyComponent(component):
    
    def RunScript(self, setView, geometry, target, vector):
        if setView:
            vp = doc.Views.ActiveView.ActiveViewport
            vp.SetCameraDirection(vector, True)
            vp.SetCameraTarget(target, True)
            bb = rs.BoundingBox(geometry)
            rs.ZoomBoundingBox(bb)
            doc.Views.ActiveView.Redraw()
        return 
