"""Compares GIS text values. Returns a True / False boolean pattern.

Determines if an attribute exists in a list of attributes.
Returns a True/False map of the attribute location in the list.
Based on the work of Jackie Berry.

    Typical usage:
        You can provide an Attribute Name by typing it on a GH Panel (note that you need to type the value that you’re comparing with the exact same characters and spaces of the value you’re expecting to find or compare) and plugin it into the AttributeName input of the component.
        You can provide an Attribute Name by selecting a specific Attribute form the original list of GIS attributes. If you choose to do it this way, you need to provide an Index Number, which is the position in the list of the attribute you want to compare (Note that the lists in grasshopper always start with zero).You can either plug a slider or a Panel with a number to the AttributeIndex input of the component. If you choose to provide an AttributeIndex, you should Flatten the AttributeIndex input and Graft the Boolean output.

    Inputs:
        AttributeList: list of attributes
        AttributeName: name of attribute you want to find in the list
        AttributeIndex: index of attribute you want to identify in the list

    Output:
        Boolean: list of booleans"""

__author__ = "palomagr"
__version__ = "2020.07.09"

#ghenv.Component.Name = "Compare GIS Attributes"
#ghenv.Component.NickName = "Compare GIS Attributes"

from ghpythonlib.componentbase
import executingcomponent as component
import Grasshopper, GhPython, System, Rhino
import rhinoscriptsyntax as rs


class MyComponent(component):

    def RunScript(self, AttributeList, AttributeName, AttributeIndex):
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
