"""
Determines if an attribute exists in a list of attributes.
Returns a True/False map of the attribute location in the list.
Inputs:
    AttributeList: list of attributes
    AttributeName: name of attribute you want to find in the list
    AttributeIndex: index of attribute you want to identify in the list
Output:
    Boolean: list of booleans
"""
from ghpythonlib.componentbase import executingcomponent as component
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
