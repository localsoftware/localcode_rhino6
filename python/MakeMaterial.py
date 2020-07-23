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
__author__ = "based on the work of chanley, Paloma Gonzalez is the author"
__version__ = "2020.07.23"
        
#ghenv.Component.Name = "Make Material"
#ghenv.Component.NickName = "Make Material"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Grasshopper as gh
import scriptcontext as sc


class MyComponent(component):
    
    def RunScript(self, Name, diffuseColor, specularColor, emissionColor, transparency,
    reflectionRange, glossiness):

        GHMaterial= None
        Material= None
        sc.doc = Rhino.RhinoDoc.ActiveDoc
        num = sc.doc.RenderMaterials.Count
        

        Rhino.DocObjects.Material.
        print('material exists')

        for i in range(num):
            mat_from_table = rs.MaterialName(i)
            if Name == mat_from_table:
                print('yes')
                
        
        newMat = Rhino.DocObjects.Material()
        if Name == None:
            print ("Add a name to the the material")
        newMat.Name = Name
        
        if diffuseColor == None:
            print ("Add a color to the material")
        newMat.DiffuseColor = diffuseColor
        
        Reflection = min(max(reflectionRange, 0), 1);
        Smoothness = min(max(glossiness, 0), 1);    
        
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
        
        
        sc.doc = ghdoc
        # return outputs if you have them; here I try it for you:
        return (Material, GHMaterial)
