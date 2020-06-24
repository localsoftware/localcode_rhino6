"""Generates geometry from GH to Rhino with attributes.
    Inputs:
        G: Geometry to bake
        L: Layer name for bake
        B: Boolean bake Activate
    Output:
        a: The a output variable"""

__author__ = "palomagr"
__version__ = "2020.06.24"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System, Rhino, os
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import ghpythonlib.components as ghcomp
import scriptcontext as sc
rcdoc = Rhino.RhinoDoc.ActiveDoc
ghdoc = sc.doc

class MyComponent(component):

if B:
    
    print(type(G)) #debug message to Python output
    
    #we obtain the reference in the Rhino doc
    doc_object = rs.coercerhinoobject(G, True, True)
    print(type(doc_object))
    
    attributes = doc_object.Attributes
    print('the type of attributes is: ' + str(type(attributes)))     #debug message to Python output

    geometry = doc_object.Geometry
    print('the type of geometry is: ' + str(type(doc_object)))     #debug message to Python output
    
    #we change the scriptcontext
    scriptcontext.doc = Rhino.RhinoDoc.ActiveDoc
    
    #we add both the geometry and the attributes to the Rhino doc
    rhino_brep = scriptcontext.doc.Objects.Add(geometry, attributes)
    print('the Rhino doc ID is: ' + str(rhino_brep))     #debug message to Python output
    
    #we can for example change the layer in Rhino...
    if not rs.IsLayer(L): 
        rs.AddLayer(L)
    rs.ObjectLayer(rhino_brep, L)
    
    #we put back the original Grasshopper document as default
    scriptcontext.doc = ghdoc
    a = G
return:
