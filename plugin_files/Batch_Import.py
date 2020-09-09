from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import ghpythonlib.treehelpers as th
import os
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML


rcdoc = Rhino.RhinoDoc.ActiveDoc
ghdoc = sc.doc

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "BatchImport", "BatchImport", """Imports geometry from Rhino files into GH, preserves layers' hierarchy as a data tree.
Imports .3dm files into Rhino and Grasshopper. 
The component can erase existing geometry in the Rhinodoc.
    Typical usage:
Takes a number of files and imports their geometries to GH.
You need to provide a path for the folder that contains the files to be imported.
Use the string concatenate component to join the file path of the folder with the number/name of the file to be imported.
You can specify the file number with a slider.
Use another string concatenate component to concatenate the file extension to the file path of the files and plug it into the FilePaths input of the component.
Based on the work of Jackie Berry.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("5ae80faf-486f-463d-a98c-71d290793707")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "filenames", "filenames", "The x script variable")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "sourceFolderPath", "sourceFolderPath", "Script input sourceFolderPath.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "Import", "Import", "boolean to activate the import")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "deleteExisting", "deleteExisting", "boolean to delete existing geometry in file")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "geometryOut", "geometryOut", "The imported geometry into GH space.")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "status", "status", "Script output status.")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        result = self.RunScript(p0, p1, p2, p3)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAAJlSURBVEhLxZVNaxNRFIZTauzED7TB0FQSmxZDMDQkbjS2apIm1VaIoC4EcSG4cKEiCoJuFOpGKmhQsyxSQVSsiogfC40rf4CbgogWdCEiirViKyYe37e5Z2GcFNrE+sBDyDv3npM5c5k45hsLrjAuYAAWQrdRMyeszBrhMqNmf7EPjhtjDMAO+NkYZwAyULMkA7AefjT2MbDjKBSjFmNTzXoYADbVLMsApKFmuxnY0Q3z8DL0MwC8k5yxnQEIwUFjkAEIQM3CDP4LbXC7kQ+LtMJtxmYGwAM144Egy2Ev3AJ53ZZDUOe4jgHYCzVLMACcu2b9DACvabaTgR3/vIEPcgOP2VIGoAVqxjEQnn8eVapj40g107HND9GA3ypEIkueRTpd9RP1fD7rKRtk8+fXiEhGSuMbpfildllHpFfOnAryeTg87asWPx65Hp1uIsWEyPfNIpNzkPtK2I86V4c6xb+y6Q4bKAPHDgekNJXCgqTI100iE7OQ67FvaiIpB/b7+ctPlMv+STaVcH94/bILi3tEvlUUqSbXYf3oi7hsiLvfog7fS1Vpa/W6CndvcWTp8q1XuxvmP3Ad664NR8Ttth5gv7dcZmYa4ODJ4x0iPzGyX5hrZRMzkuJkSo4cDHAkp6d3zpJd/WnPp3dveCowMi1uRvJqtEtS3c3vsY7vpDmzOuBb9PzhvbU4IXj4LF5Myu0bUfG2uJ7gur7WawJ/gQ1XCo9iGFdG7o/EOJJL5Uv1Y+vN4RBG0ydD+TAb6D9e3dhz8VxQxsZScnYgxAY1zd2OsNPZmLOsphw+L+B7RzmeCYfjN6Hu2rXbx7TKAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    

        
    """
    Deletes existing geometry from Rhino file before import.
    """
    def deleteExistingGeom(self):
        sc.doc = Rhino.RhinoDoc.ActiveDoc
        objects = rs.AllObjects()
        if objects:
            for obj in objects:
                rs.DeleteObject(obj)
        layers = rs.LayerNames()
        for layer in layers:
            if layer!=rs.CurrentLayer():
                rs.DeleteLayer(layer)
        return

    """
    Imports geometry from files

    """
    def importRhinoFile(self, fileNames, sourcePath, Import):

        #file import
        for fn in fileNames:
            thisFilePath = os.path.join(sourcePath,fn)
            importCommandString = '_-Import "' + thisFilePath + '" _Enter'
            imported = rs.Command(importCommandString, echo=False)

            if not imported:
                print "there was a problem with file: " + fn
                self.AddRuntimeMessage(RML.Warning,"there was a problem with file: " + fn)

        return


    """
    Grabs geometry from Rhino and constructs data tree.
    Each branch of the tree is a different layer in the document.
    """
    def rhinoGeomToDataTree(self):
        sc.doc = rcdoc
        layers = rs.LayerNames(sort=False)
        sc.doc = ghdoc
    #    layerTree = [[] for layer in layers]
        layerTree = []
        for i in range(len(layers)):
            objs = Rhino.RhinoDoc.ActiveDoc.Objects.FindByLayer(layers[i])

            if objs:
                geoms = [obj.Geometry for obj in objs]
    #            layerTree[i].extend(geoms)
                layerTree.append(geoms)
        status= str(len(layerTree))+ " branches \n"

        layerTree = th.list_to_tree(layerTree, source=[])

        return layerTree, status

    def RunScript(self, filenames, sourceFolderPath, Import, deleteExisting):
        geometryOut, status = None, None
        if filenames == None:
            self.AddRuntimeMessage(RML.Warning, "Add filenames.")
        if sourceFolderPath == None:
            self.AddRuntimeMessage(RML.Warning, "Add a source Folder Path as a string.")
        if Import == None:
            self.AddRuntimeMessage(RML.Warning, "Add a boolean toggle to the 'Import' input.")
        #Perform Import
        if Import:
            # option to delete existing geometry in document
            status = "start import \n"
            if deleteExisting:
                self.deleteExistingGeom()
                status += "deleted \n"

            #now import geometry from files
            if (filenames != None) and (sourceFolderPath != None):
                #import function here
                self.importRhinoFile(filenames, sourceFolderPath)
                status += "imported rhino files \n"
#                thisDoc.ScheduleSolution(20, self.rhinoGeomToDataTree)
                geometryAndStatus=self.rhinoGeomToDataTree()
                geometryOut = geometryAndStatus[0]
                status+=geometryAndStatus[1]
                status += "geometry to datatree \n"
            else:
                if filenames==[]:
                    print "Provide a list of filenames"
                    self.AddRuntimeMessage(RML.Warning,"Provide a list of filenames")
                if sourceFolderPath==None:
                    print "Provide the path to your source folder"
                    self.AddRuntimeMessage(RML.Warning,"Provide the path to your source folder")

        # return outputs if you have them; here I try it for you:
        return (geometryOut, status)


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "BatchImport"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("afe9ee0a-66e4-473d-a7eb-063849a8b82e")