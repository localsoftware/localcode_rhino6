"""Creates a new Material.
    Inputs:
        Name: name strin
        diffuseColor: difusse color
        specualrColor: specular color
        emissioColor: emission color
        transparency: transparency from 0 to 1
        reflectionRange: reflection range from 0 to 1 
        glossiness: glossiness from 0 to 1
"""
__author__ = "chanley"
__version__ = "2019.02.04"
        
#ghenv.Component.Name = "Make Material"
#ghenv.Component.NickName = "Make Maaterial"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Grasshopper as gh


class MyComponent(component):
    
    def RunScript(self, Name, diffuseColor, specularColor, emissionColor, transparency,
    reflectionRange, glossiness):

        GHMaterial= None
        Material= None
        
        if Name == None:
            print ("Add a name to the the material")
        
        if diffuseColor == None:
            print ("Add a color to the material")
        
        
        Reflection = min(max(reflectionRange, 0), 1);
        Smoothness = min(max(glossiness, 0), 1);
        
        newMat = Rhino.DocObjects.Material()
        
        newMat.Name = Name
        newMat.DiffuseColor = diffuseColor
        
        if specularColor != None:
            newMat.SpecularColor = specularColor
            newMat.ReflectionColor = specularColor

        if emissionColor != None:
            newMat.EmissionColor = emissionColor
            
        if transparency != None:
           newMat.Transparency = transparency
        else: 
            newMat.Transparency = 0

        if glossiness != None:
            newMat.ReflectionGlossiness = Smoothness

        newMat.Reflectivity = Reflection
        newMat.AmbientColor = diffuseColor
        material_gh = Rhino.Render.RenderMaterial.CreateBasicMaterial(newMat) 
        GHMaterial= gh.Kernel.Types.GH_Material(material_gh) # GH preview material
        Material = material_gh # Rhino Material
        
        
        # return outputs if you have them; here I try it for you:
        return (Material, GHMaterial)
