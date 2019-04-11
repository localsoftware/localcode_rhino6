import os
import time

import Rhino
import cPickle as pickle
import rhinoscriptsyntax as rs
from scriptcontext import doc


if setView:
    vp = doc.Views.ActiveView.ActiveViewport
    vp.SetCameraDirection( vector, True)
    vp.SetCameraTarget(target, True)
    bb = rs.BoundingBox(geometry)
    rs.ZoomBoundingBox( bb)
    doc.Views.ActiveView.Redraw()