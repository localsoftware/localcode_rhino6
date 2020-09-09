from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System, Rhino, os
import rhinoscriptsyntax as rs
import ghpythonlib.treehelpers as th
import ghpythonlib.components as ghcomp
import scriptcontext as sc
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML


rcdoc = Rhino.RhinoDoc.ActiveDoc
ghdoc = sc.doc


class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "BatchExport", "BatchExport", """Exports geometry to a new file or to multiple new files.
This component exports GH geometry structured as a tree into files.
The output file number is the same as the number of input file names.
The output file extensions can be .3DM, .DWG, .SVG, or .AI.
Based on the work of Jackie Berry.
    Typical usage example:
Input geometry as branches, a list of file names, an export file path, and a boolean to activate the component.
The Layer names list, colors list, and 'delete existing' boolean inputas are optional.
When 'Export' is set to 'True', files will be created.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("a1ff11d2-e062-41d0-bd93-5503dc532301")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "geometry", "geometry", "Data tree of geometries. Every branch corresponds to a layer.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "exportFileName", "exportFileName", "Export file name.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "exportFilePath", "exportFilePath", "Target directory.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "layerNames", "layerNames", "List of layer names to bake geometry into.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "layerColors", "layerColors", "List of colors (Optional). Can be one color or as many colors as layer names.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "Export", "Export", "boolean to run component")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "deleteExisting", "deleteExisting", "boolean to delete geometry already in document.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        pass    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        p5 = self.marshal.GetInput(DA, 5)
        p6 = self.marshal.GetInput(DA, 6)
        result = self.RunScript(p0, p1, p2, p3, p4, p5, p6)

        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAAJuSURBVEhLvZRNaBNBGIY3FkUTi1ol/bOSEkkiokjtQdrUkh8bK8Glrdh4KBWq6EUPevCgWH8gaCuCIIgeAl7Eg3oQlYII6kW8iUcVSlGqqBSpxUot+XzfmR2omNaYrj7wEPbd+WY2386s9T/wws2w8R/Iea1UT6ZWBgbCku1fK9lTLoh5Bgcj0mVXCxdoOnIoICLbYRLGXXAbTMm+3jq1AMmk2/1fRkeiuBET+dpSulhg+FWzxGMVHzGvrafXRIJrfM8fPmjAoITItwLFszkOJ7equru3N0ldjfcJ5qvX0/7KIsvyXMmeCaknkelWXVxoUiPv5zFuOiYnjgXZkgtwgZptDvZ22FUTn0ZR/KeW4f674WZJJf1jqNuty4tjYyRU/uLpo8bfW6ZawskTMnSvQeoDvmcYH9Jlf4e3zFOWu3g+rFs2hT5z8h9oST4uZ7Ed0dLLGLdQDy+dA5numvHPH7DLvrfK+7dR6bRVS3r0bXfou5GL4J+0ydVL6/gyd+nYPez7t9ZjgbTcvL6BC8R07B4dnTv90n8yLOn2Si6Q0LF78KMYhDxA/F0MS8YDV8MAXMnAYQlcAbmYoRxWQT9kXVH44AicgtcYOAzBSfhYXWnOwQn4Bs5ceE6Wwjxkr+8wcHgJmb1WV5ocZEZZVxQ8OEfhaTjzi9gLmfWpK00SHoeH4bwP3Lzh7uDppKsYAL7sjCNfJKmEJqtmACpgl2Mtg0IchKafUQZgDzRZGwOwA5rMtJDjTcaaguyHZlATA8BPsMnM4UpBk6UZAI432ayfbf71Fsin4f4mPAfM6DIGzu8Wx+UMAHeQydguYFk/ATL702eHHBctAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))


    def RunScript(self, geometry, exportFileName, exportFilePath, layerNames, layerColors, Export, deleteExisting):
        if geometry == None:
            self.AddRuntimeMessage(RML.Warning, "Add geometry in branches.")
        if exportFileName == None:
            self.AddRuntimeMessage(RML.Warning, "Add a export File Name.")
        if exportFilePath:
            self.AddRuntimeMessage(RML.Warning, "Add a export File Path.")

        def bake(geometry, layerNames, layerColors):
            geometryList = [geometry.Branch(b) for b in range(geometry.BranchCount)]
        #    print geometryList
            if len(geometryList) != len(layerNames):
                print "The number of layers must match the number of branches"
                self.AddRuntimeMessage(RML.Error,"The number of layers must match the number of branches")
                return
            elif len(layerColors)!=len(layerNames) or layerColors==[]:
                self.AddRuntimeMessage(RML.Warning, "The number of layer colors must match the number of layers.")
                print "The number of layer colors must match the number of layers."
            else:
                attr= Rhino.DocObjects.ObjectAttributes()
                sc.doc = rcdoc

                for i in range(len(geometryList)):
                    currentLayer= layerNames[i]
                    if layerColors== None:
                        currentColor= None
                    else:
                        currentColor=layerColors[i]

                    #if layer does not exist, make the layer and assign layer color
                    if not rs.IsLayer(currentLayer):
                        print "layer doesn't exist"
                        if layerColors!= None:
                            rs.AddLayer(name= currentLayer, color= currentColor)
                    #if layer exists, check and assign layer color
                    if currentColor!=None and rs.LayerColor(currentLayer)!=currentColor:
                        rs.LayerColor(currentLayer, currentColor)

                    #get index of current layer
                    layerIndex = rs.LayerOrder(currentLayer)

                    #get objects on this branch

                    for id in geometryList[i]:
                        sc.doc = ghdoc
                        gh_to_rhino = rs.coercerhinoobject(id)

                        #set object layer
                        objAttr = gh_to_rhino.Attributes
                        objAttr.LayerIndex = layerIndex
                        #separate geometry
                        objGeom = gh_to_rhino.Geometry

                        #bake!
                        sc.doc=rcdoc
                        rcdoc.Objects.Add(objGeom, objAttr)
            return


        """
        Export geometry in file to file name
        """
        def export():
            #select objects to export
            sc.doc= rcdoc
            rs.AllObjects(select=True)
            filepath = os.path.join(exportFilePath, exportFileName)
            exportCommandString = '_-Export "' + filepath + '" _Enter _Enter _Enter'
            out = rs.Command(exportCommandString, echo=True)
            sc.doc=ghdoc
            return


        """
        deletes all existing geometry from document.
        """
        def deleteExistingGeom():
            sc.doc = rcdoc
            allObjs = rs.AllObjects()
            rs.DeleteObjects(allObjs)
            sc.doc = ghdoc
            return

        """
        Meat of the component
        """
        if Export:
            if (geometry!=None) and (exportFileName!=None) and (exportFilePath!=None)\
            and (layerNames!=None) and (layerColors!=[]):
                if deleteExisting:
                    deleteExistingGeom()
                bake(geometry, layerNames, layerColors)
                export()
                
            elif geometry==None:
                print "Please add input geometry"
            elif exportFileName==None:
                print "Please specify a name for your export file."
            elif exportFilePath==None:
                print "Please specify a destination directory for your export."
            elif layerNames==None:
                print "Please specify target layers for each branch of your geometry."
            elif layerColors==[]:
                print "Please add layer colors."

        return


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "BatchExport"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("52e31e47-d50a-46b1-b138-9317d902a14f")