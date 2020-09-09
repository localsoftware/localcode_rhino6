"""Creates a new Material.

Returns a new Material, a Render Material and a GH Preview Material using the parameters set as inputs.
To bake into Rhino you need to use the 'Bake with Attributes' LocalCode component. The material will be baked into a layer.
Based on the work of Chris Hanley.

    Typical usage:
        Input a name and a diffuse color and create a material.
        The rest of the inputs are optional.
        Use the 'Material' output to assign the material to a geometry.
        Plug the 'GHMaterial' output to a 'Preview' component to visualize your material on GH objects.

    Inputs:
        Name: name string
        diffuseColor: diffuse color
        specularColor: specular color
        emissioColor: emission color
        transparency: transparency from 0 to 1
        reflectionRange: reflection range from 0 to 1
        glossiness: glossiness from 0 to 1

    Outputs:
        Material: Render material for Rhino geometry
        GHMaterial: Material for GH preview """

__author__ = "palomagr"
__version__ = "2020.07.09"

# ghenv.Component.Name = "Make Material"
# ghenv.Component.NickName = "Make Material"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import Grasshopper as gh
import scriptcontext as sc


class MyComponent(component):

    def RunScript(self, Name, diffuseColor, specularColor, emissionColor, transparency,
                  reflectionRange, glossiness, create):
        GHMaterial = None
        Material = None
        newMat = ''

        if create:
            sc.doc = Rhino.RhinoDoc.ActiveDoc
            num = sc.doc.RenderMaterials.Count

            for i in range(num):
                mat_from_table = rs.MaterialName(i)
                if Name == mat_from_table:
                    rs.ResetMaterial(i)
                    newMat = sc.doc.Materials[i]
                else:
                    newMat = Rhino.DocObjects.Material()

            Reflection = min(max(reflectionRange, 0), 1);
            Smoothness = min(max(glossiness, 0), 1);

            if Name != '':
                newMat.Name = Name
            else:
                newMat.Name = 'custom'

            if diffuseColor != None:
                newMat.DiffuseColor = diffuseColor
            else:
                newMat.DiffuseColor = [255, 255, 255]

            if specularColor != None:
                newMat.SpecularColor = specularColor
                newMat.ReflectionColor = specularColor

            if emissionColor != None:
                newMat.EmissionColor = emissionColor

            if transparency != None:
                newMat.Transparency = transparency

            if glossiness != None:
                newMat.ReflectionGlossiness = Smoothness

            newMat.Reflectivity = Reflection
            newMat.AmbientColor = diffuseColor
            material_gh = Rhino.Render.RenderMaterial.CreateBasicMaterial(newMat)
            GHMaterial = gh.Kernel.Types.GH_Material(material_gh)  # GH preview material
            Material = material_gh  # Rhino Material

        # return outputs if you have them; here I try it for you:
        return (Material, GHMaterial)
