"""Set the current Rhino viewport to a camera view.

Once you have a camera created, the Set View component easily adjusts the view to it.
You can use these views to batch render, export or create presentation drawings from GH geometries easily.
Based on the work of Jackie Berry.

    Typical usage:
        Once you have created a view with the Create View component, simply plug the Geometry, View Vector,
        and View Target outputs into the geometry, vector, and target inputs of the component.
        Once you have a view created, you can easily adjust the view with it. You can use these views to batch render.
        Add a Boolean Toggle component to activate and deactivate the view change.

    Inputs:
        SetView: boolean to set view
        geometry: geometry in view
        target: 3D point defining camera target
        vector: 3D vector defining camera direction

    Outputs:
        None"""

__author__ = "palomagr"
__version__ = "2020.07.09"

#ghenv.Component.Name = "Set View"
#ghenv.Component.NickName = "Set View"

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
