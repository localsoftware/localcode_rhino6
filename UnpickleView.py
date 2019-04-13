import os
import time

import Rhino
import cPickle as pickle
import rhinoscriptsyntax as rs
from scriptcontext import doc

if UnPickle:
    f = open(path + '%sview' % int(siteNumber), 'rb')
    view = pickle.load(f)
    f.close()
    if len(view) == 3:
        geometry = view[0]
        vector = Rhino.Geometry.Vector3d(view[1])
        target = view[2]
    else:
        print 'bad view data'
    
    vp = doc.Views.ActiveView.ActiveViewport
    vp.SetCameraDirection( vector, True)
    vp.SetCameraTarget(target, True)
    bb = geometry.GetBoundingBox(True)
    vp.ZoomBoundingBox( bb)
    doc.Views.ActiveView.Redraw()
    #return view


