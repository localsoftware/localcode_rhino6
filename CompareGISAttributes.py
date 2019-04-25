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
