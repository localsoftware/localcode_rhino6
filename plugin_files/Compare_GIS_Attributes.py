from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython, System, Rhino
import rhinoscriptsyntax as rs
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "CompareGISAttributes", "CompareGISAttributes", """Compares GIS text values. Returns a True / False boolean pattern.
Determines if an attribute exists in a list of attributes.
Returns a True/False map of the attribute location in the list.
Based on the work of Jackie Berry.
    Typical usage:
You can provide an Attribute Name by typing it on a GH Panel (note that you need to type the value that you’re comparing with the exact same characters and spaces of the value you’re expecting to find or compare) and plugin it into the AttributeName input of the component.
You can provide an Attribute Name by selecting a specific Attribute form the original list of GIS attributes. If you choose to do it this way, you need to provide an Index Number, which is the position in the list of the attribute you want to compare (Note that the lists in grasshopper always start with zero).You can either plug a slider or a Panel with a number to the AttributeIndex input of the component. If you choose to provide an AttributeIndex, you should Flatten the AttributeIndex input and Graft the Boolean output.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("3578c0fb-d2fd-4f61-91b5-0d935f145152")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "AttributeList", "AttributeList", "list of attributes")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "AttributeName", "AttributeName", "name of attribute you want to find in the list")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "AttributeIndex", "AttributeIndex", "index of attribute you want to identify in the list")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "Boolean", "Boolean", "list of booleans")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAANeSURBVEhLtVVpSJRhEE4jy8pzI6zVvNNM3Vg1a9V1d20tihLsTz+KDgwK8kf1oyw7LUoTutgCidKIig4rtssEIy3JrCg6IKSDLoSSIi23LJ+e+da1JbUNtz54+OabeWeed+Z9Z74BfGYQJf8RAywb10TBatXCekLz72BNQv7SMAhBSe0VLYAphOE3ZBFmwtkmOlOXLG+xC4xdOgfMOHoo3k5wsVJjV7Zm/AK/79Qlo2BlKM4eTwR+0N6uR12VFo9vTwRsBrx/lYYNBeEo2xNLWybw2dnfiAOWuD4IvhvQUJtM40Co1cP49sCx8niuyYZJH4DNhVGUpyBDp4IqcAg8PQeiaJ3omMVfETB1o16FBXNHU56GbZuiEBHmQzkbOTNU2L0jBu9e6BCiHk5dFs6fTETQyKHodM6iTwKW4cu7dARz5w8aUqg3oeOjHpVHWSYGm9VF0MLy+PkNwf1bLBfX1NdMQOdH+re5IujQ4/mjSQgd44PW5nQ0PUzFhdMa3Ku3k0kGJUXRlM2YOX2kBMDs3CC0teiBb8xAYrgieMagQoB2A7ZuiOYiD/j7DeJBZyI3ZwRLJgS8Td+NKC0eCz9fL+hSA9HZwTNwWSKbXtm5evQwNN1LRTtL9qgxBTHRrDdtQmDZGYsbNVoUroqg31S8fjIZI1TeePNkErNgJn8kkBqyFBm6QCxeGEx5Guqqk7hLZkBnIdi3Kxb365Pg7e0F2ycD3jbpMCpoqHLw+OqKQMA7f/Oa/ZpGRvjw7Yk8hcwMU6Z/9zVN1gZAFTAYvj5emDtHrQR1fcgOcEEjeyF/STAO7h+n1Bu2TNRc0PB2JXOn0mjpWM1G3LQ2HLYP3DnL6ezfk0CBtLwDMhayCedRIGND9CLLqBC7QGSHnz1ON8GlM0JgREVZArZvjkFxUf8h/qeOSLwsJwIlAyNnTwquXtS6jQcN9ubrkcHNmiRUndWg6pwboP/dGzyjngQmHC8fj90lkW7DeiKB8ZxK5DjklpdpaH6qQ/MzN0D/D6/TlIp0E1zuymBncRyWL4vEivz+Q/wPWGS095KB8tPg/HEfjNNbBlvWRyNvvtpt7C3lH4790k1wvVr+ydJMZIewuwuJk81Lk6AQWFbkh6OcHxVl43G4LN5tSJyK8kQsmheCn2zslj+FwMYUAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))


    def RunScript(self, AttributeList, AttributeName, AttributeIndex):
        if AttributeList == None:
            self.AddRuntimeMessage(RML.Warning, "Add an Attribute List.")
        if AttributeName == None:
            self.AddRuntimeMessage(RML.Warning, "Add an Attribute Name.")
        if AttributeIndex == None:
            self.AddRuntimeMessage(RML.Warning, "Add an Attribite Index.")
        Boolean = None
        attribs = AttributeList

        attributes = []
        for attribute in attribs:
            if type(attribute) == int or float:
                attributes.append(str(attribute.strip()))
            else:
                attributes.append(attribute.strip())

        if AttributeName != None and AttributeIndex == None:
            bool = []
            for attribute in attributes:
                bool.append(attribute == str(AttributeName))

        elif AttributeName == None and AttributeIndex != None:
            selected_attrib = attributes[int(AttributeIndex)]
            bool = []
            for attribute in attributes:
                bool.append(attribute == str(selected_attrib))

        elif AttributeName != None and AttributeIndex != None:
            bool = 'You can compare either based on an AttributeName or an AttributeIndex, but not from both'

        else:
            bool = 'You need to provide an AttributeName or an IndexNumber to compare'

        Boolean = bool

        # return outputs if you have them; here I try it for you:
        return Boolean


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "CompareGISAttributes"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("3101efa8-44bf-4ac1-a4d5-8a8855bd1286")