"""Imports geometry from GeoJSON files into grasshopper.

Preserves layer hierarchy as data tree.
The Import GeoJSON component extracts the GIS attributes from the geoJSON files.
Based on the work of Jackie Berry.
   
    Typical usage:
        Input a path as a string.

    Inputs:
        Import: boolean to start import
        geoJSONFolderPath: path to folder with GeoJSON files
        siteNumber: int site number

    Output:
        Geometry: The imported geometry ingo gh space
        Attributes: attributes of objects / layers
        Values: evaluated values
        LayerNames: list of layer names"""

__author__ = "palomagr"
__version__ = "2020.07.09"

#ghenv.Component.Name = "Import GeoJason"
#ghenv.Component.NickName = "Import GeoJSON"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino, json

# Import standard library modules
from Rhino.Geometry import *
from scriptcontext import doc

# import .NET libraries
from System import Object
import rhinoscriptsyntax as rs
import sys, os

# import GH dependencies
from clr import AddReference as addr
addr("Grasshopper")
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path

class MyComponent(component):

    def RunScript(self, Import, geoJSONFolderPath, SiteNumber):
        Geometry, Attributes, Values, LayerNames = None, None, None, None
        def addRhinoLayer(layerName, layerColor=System.Drawing.Color.Black):
            """Creates a Layer in Rhino using a name and optional color. Returns the
            index of the layer requested. If the layer
            already exists, the color is updated and no new layer is created."""
            docLyrs = doc.Layers
            layerIndex = docLyrs.Find(layerName, True)
            if layerIndex == -1:
                layerIndex = docLyrs.Add(layerName,layerColor)
            else: # it exists
                layer = docLyrs[layerIndex] # so get it
                if layer.Color != layerColor: # if it has a different color
                    layer.Color = layerColor # reset the color
            return layerIndex


        def PointToRhinoPoint(coordinates):
            if len(coordinates) > 2:
                z = coordinates[2]
            else:
                z = 0.0
            x, y = coordinates[0], coordinates[1]
            return Point3d(x, y, z)


        def MultiPointToRhinoPoint(coordinates):
            rhPointList = []
            for point in coordinates:
                rhPointList.append(PointToRhinoPoint(point))
            return rhPointList


        def MeshToRhinoMesh(coordinates, faces):
            rhMesh = Mesh()
            for point in coordinates:
                rhPoint = PointToRhinoPoint(point)
                rhMesh.Vertices.Add(rhPoint)
            for face in faces:
                i, j, k = tuple(face)
                mFace = MeshFace(i, j, k)
                rhMesh.Faces.AddFace(mFace)
            rhMesh.Normals.ComputeNormals()
            rhMesh.Compact()
            return rhMesh


        def LineStringToRhinoCurve(coordinates):
            rhPoints = MultiPointToRhinoPoint(coordinates)
            return Curve.CreateControlPointCurve(rhPoints, 1)


        def MultiLineStringToRhinoCurve(coordinates):
            rhCurveList = []
            for lineString in coordinates:
                rhCurveList.append(LineStringToRhinoCurve(lineString))
            return rhCurveList


        def PolygonToRhinoCurve(coordinates):
            # each ring is a separate list of coordinates
            ringList = []
            for ring in coordinates:
                ringList.append(LineStringToRhinoCurve(ring))
            return ringList


        def MultiPolygonToRhinoCurve(coordinates):
            polygonList = []
            for polygon in coordinates:
                polygonList.append(PolygonToRhinoCurve(polygon))
            return polygonList


        def GeometryCollectionToParser(geometries):
            pass # I need to figure this one out still


        def addPoint(rhPoint, objAtt):
            return doc.Objects.AddPoint(rhPoint, objAtt)


        def addPoints(rhPoints, objAtt):
            guidList = []
            for rhPoint in rhPoints:
                guidList.append(doc.Objects.AddPoint(rhPoint, objAtt))
            return guidList


        def addCurve(rhCurve, objAtt):
            return doc.Objects.AddCurve(rhCurve, objAtt)


        def addCurves(rhCurves, objAtt):
            guidList = []
            for curve in rhCurves:
                guidList.append(addCurve(curve, objAtt))
            return guidList


        def addPolygon(ringList, objAtt):
            # for now this just makes curves
            # but maybe it should make TrimmedSrfs
            # or should group the rings
            return addCurves(ringList, objAtt)


        def addPolygons(polygonList, objAtt):
            guidList = []
            for polygon in polygonList:
                # !! Extending the guid list !!!
                guidList.extend(addPolygon(polygon, objAtt))
            return guidList


        def addMesh(rhMesh, objAtt):
            return doc.Objects.AddMesh(rhMesh, objAtt)


        def setUserKeys(properties, objAttributes):
            for key in properties:
                objAttributes.SetUserString(key, str(properties[key]))
            return objAttributes


        def jsonToRhinoCommon(jsonFeature):
                # deal with the geometry
                geom = jsonFeature['geometry']
                geomType = geom['type'] # this will return a mappable string
                coordinates = geom['coordinates']
                # if this is a mesh, pass the faces
                if geomType == 'Mesh':
                    faces = geom['faces']
                    rhFeature = geoJsonGeometryMap[geomType][0](coordinates, faces)
                # translate the coordinates to Rhino.Geometry objects
                else:
                    rhFeature = geoJsonGeometryMap[geomType][0](coordinates)
                return rhFeature


        def addJsonFeature(jsonFeature, objAttributes):
                # deal with the properties
                if jsonFeature['properties']:
                    objAttributes = setUserKeys(jsonFeature['properties'], objAttributes)
                geomType = jsonFeature['geometry']['type']
                rhFeature = jsonToRhinoCommon(jsonFeature)
                # return the GUID(s) for the feature
                return geoJsonGeometryMap[geomType][1](rhFeature, objAttributes)


        def processGeoJson(parsedGeoJson,
                 destinationLayer=None,
                 destinationLayerColor=System.Drawing.Color.Black):
            # get the features
            jsonFeatures = parsedGeoJson['features']
            guidResults = []
            # set up object attributes
            for jsonFeature in jsonFeatures: # for each feature
                att = Rhino.DocObjects.ObjectAttributes()
                # setup layer if requested
                if destinationLayer != None:
                    destinationLayer = None
                    #att.LayerIndex = addRhinoLayer(destinationLayer,
                                                   #destinationLayerColor)
                guidResults.append(addJsonFeature(jsonFeature, att))
            # return all the guids
            return guidResults


        def load(rawJsonData,
                 prefix=None,
                 destinationLayer=None,
                 destinationLayerColor=System.Drawing.Color.Black):
            # if the data already appears to be a dict literal ...
            if type(rawJsonData) == dict:
                jsonData = rawJsonData
            else: # otherwise, just try to load it
                jsonData = json.loads(rawJsonData)
            # if this is just a GeoJSON ...
            if jsonData["type"] == "FeatureCollection":
                # process the GeoJSON, pass the layer and color in
                return processGeoJson(jsonData, destinationLayer,
                                      destinationLayerColor)
            # or if this is a set of layers from PostSites ...
            elif jsonData["type"] == "LayerCollection":
                # make a list for all the guids
                allResults = []
                layersList = jsonData['layers']
                for layer in layersList: # for each layer
                    name = prefix + layer['name'] # get the name, modified to add filename to
                    if 'color' in layer: # get the color if it exists
                        color = layer['color']
                    else:
                        color = destinationLayerColor # or just make it black
                    geoJson = layer['contents'] # get the GeoJSON for this layer
                    # make it
                    layerResults = processGeoJson( geoJson, name, color )
                    allResults.append(layerResults)
                return allResults, layersList
            else:
                return "This doesn't look like correctly formatted GeoJSON data.\nI'm not sure what to do with it, sorry."


        def getAttsVals(id,path=None):
            objct = doc.Objects.Find(id)
            data = objct.Attributes.GetUserStrings()
            d = {}
            k = []
            v = []
            if path==None:
                for u in sorted(data):
                    k.append(u)
                    print k
                    d[u] = data[u]
                    v.append(d[u])
                U = d
                Atts = k
                Vals = v
                return Atts,Vals
            if path:
                for u in data:
                    k.append(u)
                    d[u] = data[u]
                    v.append(d[u])
                    Attributes.Add(u,path)
                    Values.Add(d[u],path)
                return None,None


        def importSitefolder(filepath):
            f = str(SiteNumber)
            prefix = str(f +"_")

            try:
                thisfilepath = os.path.join(filepath, f)
                f = open(thisfilepath,'r')
            except:
                f = str(SiteNumber)+".txt"
                thisfilepath = os.path.join(filepath, f)
                f = open(thisfilepath,'r')
            myGeoJson = f.readline()
            guidList,layersList = load(myGeoJson, prefix)
            idsOut.append(guidList)
            layerNamesOut.append(layersList)
            f.close()



        def constructTree():
            ### NOTE: some problems with mutlipolygons being nested 'up' a level. This problem is rooted in 'loader'
            ### it needs to be debugged out
            for i in range (len(layerNamesOut[0])):
                p = GH_Path(i)
                LayerNames.Add(layerNamesOut[0][i]['name'],p)
            for A in idsOut:#for each file
                for i in range (len(A)):# for each layer
                    try:
                        p = GH_Path(i)#make a new data tree path
                        if (len(A[i])>1):# if the datatree path has more than one item
                            for j in range (len(A[i])):# iterate
                                try:
                                    thisId = A[i][j][0]
                                    pPrime = p.AppendElement(j)
                                    Geometry.Add(thisId,p)# add each feature to the path
                                    getAttsVals(thisId,pPrime)
                                except:
                                    ### It must be a point (tuple), cannot subscript it, grab it directly
                                    try:
                                        thisId = A[i][j]
                                        pPrime = p.AppendElement(j)
                                        Geometry.Add(thisId,p)
                                        getAttsVals(thisId,pPrime)
                                    except:
                                        continue
                        else:#otherwise, the layer has only one item (it is either a 1 item layer or a multipolygon)
                            #it is a single object layer
                            try:
                                thisId = A[i][0]
                                pPrime = p.AppendElement(0)
                                Geometry.Add(thisId,p)
                                getAttsVals(thisId,pPrime)
                            except: #multipolygon is nested one level
                                print "Multipolygon found, some list-cleanup may be needed"
                                thisId = A[i][0][0]
                                pPrime = p.AppendElement(0)
                                Geometry.Add(thisId,p)
                                getAttsVals(thisId,pPrime)
                    except:
                        print 'There were some problems importing a layer, please try again with a different set of layers'
                        continue
            return



        geoJsonGeometryMap = {
                'Point':(PointToRhinoPoint, addPoint),
                'MultiPoint':(MultiPointToRhinoPoint, addPoints),
                'LineString':(LineStringToRhinoCurve, addCurve),
                'MultiLineString':(MultiLineStringToRhinoCurve, addCurves),
                'Polygon':(PolygonToRhinoCurve, addPolygon),
                'MultiPolygon':(MultiPolygonToRhinoCurve, addPolygons),
                'Mesh':(MeshToRhinoMesh, addMesh),
                'GeometryCollection':(GeometryCollectionToParser),
                }


        """
        To run the code
        """
        if Import!= None and type(Import) == bool:
            if Import == True:
                try:
                    idsOut = []
                    layerNamesOut = []
                    importSitefolder(geoJSONFolderPath)

                    if idsOut != None:
                        Geometry = DataTree[Object]()
                        Attributes = DataTree[Object]()
                        Values = DataTree[Object]()
                        LayerNames = DataTree[Object]()
                        constructTree()
                        print 'You succesfully imported a geoJSON file!'
                    else:
                        print 'There was some problem with your geoJSON file, we imported as many layers as possible!'

                except:
                    pass
        else:
            print 'To Import you need to input a boolean toggle'


        # return outputs if you have them; here I try it for you:
        return (Geometry, Attributes, Values, LayerNames)
