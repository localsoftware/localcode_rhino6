"""Extracts object attribute names and attribute values from geometries imported from SHP files.

Extracts the User Strings from geometries imported with the ReadShapefile component.
Separates the GIS Attributes into DataTrees for every GIS geometry from the shapefile.
Based on the work of Jackie Berry.

    Typical usage:
        Connect the output geometry from a ReadShapefile component into the geometry input.
        You can plug a panel to the Attributes and Values outputs to browse their specific values.
        You can select the values of specific geometries with any List Management component, such as List Item.

    Input:
        geometry: imported geometry from shapefile.

    Outputs:
        Attributes: Tree of attributes per object from shapefile
        Values: Value per attribute per object from shapefile."""

__author__ = "palomagr"
__version__ = "2020.07.09"

#ghenv.Component.Name = "ShapeFile Extract User Strings"
#ghenv.Component.NickName = "ShapeFile Extract User Strings"

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
