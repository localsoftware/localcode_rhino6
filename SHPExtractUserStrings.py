""" Extracts object attribute names and attribute values from
    imported shapefile geometry.
Input:
    geometry: imported geometry from shapefile.
Outputs:
    Attributes: Tree of attributes per object from shapefile
    Values: Value per attribute per object from shapefile.
"""
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):
    
    def RunScript(self, geometry):
        Attributes, Values = None, None
        if geometry:
            data = geometry.GetUserStrings()
            d = {}
            k = []
            v = []
            for u in data:
                k.append(u)
                d[u] = data[u]
                v.append(d[u])
            U = d
            Attributes = k
            Values = v
        
        # return outputs if you have them; here I try it for you:
        return (Attributes, Values)
