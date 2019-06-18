"""Imports geometry from shapefile
    Inputs:
        shapefile: path to shapefile
        read: boolean to run script
        moveToCenter: boolean to center imported geometry at origin
    Output:
        geometry: imported geometry from shapefile
"""
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython, System, Rhino, os, sys, System.Text
import struct, datetime, decimal, itertools
import rhinoscriptsyntax as rs
from struct import unpack
bodyname = System.Text.Encoding.Default.BodyName
sys.setdefaultencoding(bodyname)

class MyComponent(component):
    
    def RunScript(self, shapefile, read, moveToCenter):
        
        geometry=None

        def dbfreader(f):
            """Returns an iterator over records in a Xbase DBF file.
        
            The first row returned contains the field names.
            The second row contains field specs: (type, size, decimal places).
            Subsequent rows contain the data records.
            If a record is marked as deleted, it is skipped.
        
            File should be opened for binary reads.
        
            """
            # See DBF format spec at:
            #     http://www.pgts.com.au/download/public/xbase.htm#DBF_STRUCT
        
            numrec, lenheader = struct.unpack('<xxxxLH22x', f.read(32))    
            numfields = (lenheader - 33) // 32
        
            fields = []
            for fieldno in xrange(numfields):
                name, typ, size, deci = struct.unpack('<11sc4xBB14x', f.read(32))
                name = name.replace('\0', '')       # eliminate NULs from string   
                fields.append((name, typ, size, deci))
            yield [field[0] for field in fields]
            yield [tuple(field[1:]) for field in fields]
        
            terminator = f.read(1)
            assert terminator == '\r'
        
            fields.insert(0, ('DeletionFlag', 'C', 1, 0))
            fmt = ''.join(['%ds' % fieldinfo[2] for fieldinfo in fields])
            fmtsiz = struct.calcsize(fmt)
            for i in xrange(numrec):
                record = struct.unpack(fmt, f.read(fmtsiz))
                #print record#[:4]
                if record[0] != ' ':
                    continue                        # deleted record
                result = []
                for (name, typ, size, deci), value in itertools.izip(fields, record):
                    if name == 'DeletionFlag':
                        continue
                    if typ == "N":
                        value = value.replace('\0', '').lstrip()
                        if value == '':
                            value = 0
                        elif deci:
                            value = decimal.Decimal(value)
                        else:
                            value = int(value)
                    elif typ == 'D':
                        #print type(value[:4]), type(value[4:6]), type(value[6:8])
                        try:
                            y, m, d = int(value[:4]), int(value[4:6]), int(value[6:8])
                            value = datetime.date(y, m, d)
                            print value
                        except:
                            value = datetime.date(1,1,1)
                            print "We couldn't get a date for a geometry in your dbf"
                    elif typ == 'L':
                        value = (value in 'YyTt' and 'T') or (value in 'NnFf' and 'F') or '?'
                    result.append(value)
                yield result
                
        ##########################################################################
        
        class ShpFeature(object):
            """
            This is a base class for each record in a shapefile.
            each record corresponds to one row in the shapefile's dbf table.
            To clarify the distinction between a feature and a record:
            the record is the feature + the dbf data associated with the feature
            the feature is shape (or multi-shape)
            In this class, I attach the dbf data for each record to it's feature.
            """
        
            def __init__(self, shpFile, recordNumber):
                self.shpFile = shpFile
                self.recordNumber = recordNumber
                self.shapeType = shpFile.shapeType
                self.dbfData = self.readDbfData()
        
            def readDbfData(self):
                db = self.shpFile.dbfTable
                dbfData = {}
                for i in range(len(db[0])): # for each column
                        dbfData[db[0][i]] = db[self.recordNumber + 2][i]
                return dbfData
        
            def make3D(self, zVals=None):
                """
                This method will take a list of z values and use them to create a new
                attribute called points3D, which contains 3d points. ESRI shapefiles
                place z values in a separate list form x and y values for each point,
                so this essentially integrates those values to make full 3d points.
                If the number of z values does not match the number of points,
                then this method will not work.
                This method will overwrite the points3d attribute if it already exists.
                """
                # if there's not enough z values for the number of points
                # or not enough points for the number of z values
                if not zVals:
                    zVals = [0 for i in range(self.numPoints)]
                if len(zVals) != self.numPoints:
                    print "The number of Z values does not correspond to the number of points."
                    return
                # clear points3D
                self.points3D = []
                for i in range(len(zVals)):
                    z = zVals[i]
                    x = self.points[i][0]
                    y = self.points[i][1]
                    point3d = (x,y,z)
                    self.points3D.append(point3d)
        
            def chopParts(self, partlist, pointlist):
                if type(partlist) == tuple:
                    indexSpread = list(partlist)
                elif type(partlist) == list:
                    indexSpread = partlist
                else:
                    indexSpread = [partlist]
                indexSpread.append(len(pointlist))
                chunks = []
                for i in range(len(indexSpread) - 1):
                    chunks.append(pointlist[indexSpread[i]:indexSpread[i+1]])
                return chunks
        
        class ShpPoint(ShpFeature):
        
            def __init__(self, ShpFile, recordNumber):
                ShpFeature.__init__(self, ShpFile, recordNumber)
                self.parts = [0]
                self.numParts = 1
                self.numPoints = 1
                self.points = [self.shpFile._readPoint()]
                self.x = self.points[0][0]
                self.y = self.points[0][1]
                self.make3D()
        
        class ShpPointM(ShpPoint):
            def __init__(self,ShpFile, recordNumber):
        
                ShpPoint.__init__(self, ShpFile, recordNumber)
        
                self.m = self.shpFile._readZ()
                self.make3D()
        
        class ShpPointZ(ShpPoint):
            def __init__(self,ShpFile, recordNumber):
        
                ShpPoint.__init__(self, ShpFile, recordNumber)
        
                self.z = self.shpFile._readZ()
                self.m = self.shpFile._readZ()
                self.make3D([self.z])
        
        class ShpMultiPoint(ShpFeature):
        
            def __init__(self,ShpFile, recordNumber):
        
                ShpFeature.__init__(self, ShpFile, recordNumber)
                self.parts[0]
                self.numParts = 1
                self.boundingBox = self.shpFile._readBoundingBox()
                self.numPoints = self.shpFile._readNumPoints()
                self.points = self.shpFile._readPoints(self.numPoints)
                self.make3D()
        
        class ShpMultiPointM(ShpMultiPoint):
        
            def __init__(self,ShpFile, recordNumber):
        
                ShpMultiPoint.__init__(self, ShpFile, recordNumber)
                self.mBounds = self.shpFile._readZBounds()
                self.mArray = self.shpFile._readZArray(self.numPoints)
                self.make3D()
        
        class ShpMultiPointZ(ShpMultiPoint):
        
            def __init__(self,ShpFile, recordNumber):
        
                ShpMultiPoint.__init__(self, ShpFile, recordNumber)
                self.zBounds = self.shpFile._readZBounds()
                self.zArray = self.shpFile._readZArray(self.numPoints)
                self.mBounds = self.shpFile._readZBounds()
                self.mArray = self.shpFile._readZArray(self.numPoints)
                self.make3D(self.zArray)
        
        class ShpPolyLine(ShpFeature):
        
            def __init__(self,ShpFile, recordNumber):
        
                ShpFeature.__init__(self, ShpFile, recordNumber)
        
                self.boundingBox = self.shpFile._readBoundingBox()
                self.numParts = self.shpFile._readNumParts()
                self.numPoints = self.shpFile._readNumPoints()
                self.parts = self.shpFile._readParts(self.numParts)
                self.points = self.shpFile._readPoints(self.numPoints)
                self.make3D()
        
        class ShpPolyLineM(ShpPolyLine):
        
            def __init__(self,ShpFile, recordNumber):
        
                ShpPolyLine.__init__(self, ShpFile, recordNumber)
        
                self.mBounds = self.shpFile._readZBounds()
                self.mArray = self.shpFile._readZArray(self.numPoints)
                self.make3D()
        
        class ShpPolyLineZ(ShpPolyLine):
        
            def __init__(self,ShpFile, recordNumber):
        
                ShpPolyLine.__init__(self, ShpFile, recordNumber)
        
                self.zBounds = self.shpFile._readZBounds()
                self.zArray = self.shpFile._readZArray(self.numPoints)
                self.mBounds = self.shpFile._readZBounds()
                self.mArray = self.shpFile._readZArray(self.numPoints)
                self.make3D(self.zArray)
        
        class ShpPolygon(ShpFeature):
        
            def __init__(self,ShpFile, recordNumber):
        
                ShpFeature.__init__(self, ShpFile, recordNumber)
        
                self.boundingBox = self.shpFile._readBoundingBox()
                self.numParts = self.shpFile._readNumParts()
                self.numPoints = self.shpFile._readNumPoints()
                self.parts = self.shpFile._readParts(self.numParts)
                self.points = self.shpFile._readPoints(self.numPoints)
                self.make3D()
        
        class ShpPolygonM(ShpPolygon):
        
            def __init__(self,ShpFile, recordNumber):
        
                ShpPolygon.__init__(self, ShpFile, recordNumber)
        
                self.mBounds = self.shpFile._readZBounds()
                self.mArray = self.shpFile._readZArray(self.numPoints)
                self.make3D()
        
        class ShpPolygonZ(ShpPolygon):
        
            def __init__(self,ShpFile, recordNumber):
        
                ShpPolygon.__init__(self, ShpFile, recordNumber)
        
                self.zBounds = self.shpFile._readZBounds()
                self.zArray = self.shpFile._readZArray(self.numPoints)
                self.mBounds = self.shpFile._readZBounds()
                self.mArray = self.shpFile._readZArray(self.numPoints)
                self.make3D(self.zArray)
        
        class ShpMultiPatch(ShpFeature):
        
            def __init__(self, ShpFile, recordNumber):
        
                ShpFeature.__init__(self, ShpFile, recordNumber)
        
                self.boundingBox = self.shpFile._readBoundingBox()
                self.numParts = self.shpFile._readNumParts()
                self.numPoints = self.shpFile._readNumPoints()
                self.parts = self.shpFile._readParts(self.numParts)
                self.partTypes = self.shpFile._readParts(self.numParts)
                self.points = self.shpFile._readPoints(self.numPoints)
                self.zBounds = self.shpFile._readZBounds()
                self.zArray = self.shpFile._readZArray(self.numPoints)
                self.mBounds = self.shpFile._readZBounds()
                self.mArray = self.shpFile._readZArray(self.numPoints)
                self.make3D(self.zArray)
                #self.points = [self.shpFile._readPoint()]
        
        ##################################################
        
        def readAndUnpack(type, data):
            if data=='': return data
            return unpack(type, data)[0]
        
        shapeTypeDict = {
                         0:'Null Shape',
                         1:'Point',
                         3:'PolyLine',
                         5:'Polygon',
                         8:'MultiPoint',
                         11:'PointZ',
                         13:'PolyLineZ',
                         15:'PolygonZ',
                         18:'MultiPointZ',
                         21:'PointM',
                         23:'PolyLineM',
                         25:'PolygonM',
                         28:'MultiPointM',
                         31:'MultiPatch'
                         }
        
        classTypeDict = {
                        'Point':ShpPoint,
                        'PointM':ShpPointM,
                        'PointZ':ShpPointZ,
                        'MultiPoint':ShpMultiPoint,
                        'MultiPointM':ShpMultiPointM,
                        'MultiPointZ':ShpMultiPointZ,
                        'PolyLine':ShpPolyLine,
                        'PolyLineM':ShpPolyLineM,
                        'PolyLineZ':ShpPolyLineZ,
                        'Polygon':ShpPolygon,
                        'PolygonM':ShpPolygonM,
                        'PolygonZ':ShpPolygonZ,
                        'MultiPatch':ShpMultiPatch
                        }
        
        
        class ShpFile(object):
            """
            This class is instantiated using the file path to a shapefile (must contain the .shp file extension), and as soon as it is instantiated, it reads the entire shapefile.
            Once instantiated, it contains objects for each feature based on shape type (the objects are accessible using the
            .records attribute), and allows access to the shapefile data at multiple levels.
            """
        
            def __init__(self,filePath):
                self.filePath = filePath
                self.proj = self._readProjText()
                self.dbfTable = self._readDbfTable()
                self.f = open(self.filePath, 'rb')
                header = self._readFileHeader()
                self.shapeType = header[0]
                self.boundingBox = header[1]
                self.records = self._readRecords()
                self.f.close()
        
            def _readBoundingBox(self):
                xMin = readAndUnpack('d', self.f.read(8))
                yMin = readAndUnpack('d', self.f.read(8))
                xMax = readAndUnpack('d', self.f.read(8))
                yMax = readAndUnpack('d', self.f.read(8))
                bbox = (xMin, yMin, xMax, yMax)
                return bbox
        
            def _readProjText(self):
                projPath = self.filePath[0:-4] + '.prj'
                f = open(projPath, 'r')
                s = f.read()
                return s
        
        
            def _readFileHeader(self):
                self.f.seek(32)
                shapeKey = readAndUnpack('i', self.f.read(4))
                shapeType = shapeTypeDict[shapeKey]
                boundingBox = self._readBoundingBox()
                return (shapeType, boundingBox)
        
            def _readPoint(self):
                x = readAndUnpack('d', self.f.read(8))
                y = readAndUnpack('d', self.f.read(8))
                return (x,y)
        
            def _readNumParts(self):
                return readAndUnpack('i', self.f.read(4))
        
            def _readNumPoints(self):
                return readAndUnpack('i', self.f.read(4))
        
            def _readParts(self, numParts):
                partIndices = []
                for i in range(numParts):
                    partIndex = readAndUnpack('i', self.f.read(4))
                    partIndices.append(partIndex)
                return partIndices
        
            def _readPoints(self, numPoints):
                points = []
                # I removed a short chunk of code here
                # that was used to remove any two identical
                # consecutive points. Such a check is only relevant if
                # each part is being checked separately, otherwise
                # a part that begins where the other left off would be
                # messed up.
                for i in range(numPoints):
                    point = self._readPoint()
                    points.append(point)
                return points
        
            def _readZ(self):
                z = readAndUnpack('d', self.f.read(8))
                return z
        
            def _readZBounds(self):
                zMin = self._readZ()
                zMax = self._readZ()
                return (zMin,zMax)
        
            def _readZArray(self, numPoints):
                zArray = []
                for i in range(numPoints):
                    z = self._readZ()
                    zArray.append(z)
                return zArray
        
            def setZfield(self, fieldKey=None, zValue=0.0):
                # this method will erase any existing
                # z data of the geometry
                # and will replace it with values
                # from the field designated
                # by the fieldKey
                zValue = 0.0
                for record in self.records:
                    if fieldKey != None:
                        try:
                            zValue = float(record.dbfData[fieldKey])
                        except:
                            print 'There is no field by that name in the table'
                            return
                    zArray = []
                    for each in range(record.numPoints):
                        zArray.append(zValue)
                    record.make3D(zArray)
        
            def _readDbfTable(self):
                dbfFile = self.filePath[0:-4] + '.dbf'
                dbf = open(dbfFile, 'rb')
                db = list(dbfreader(dbf))
                dbf.close()
                return db
        
            def _readRecords(self):
                records = []
                self.f.seek(100)
                iterator = 0
                while True:
                    record = self._readFeature(iterator)
                    if record == False:
                            break
                    records.append(record)
                    iterator += 1
                return records
        
            def _readFeature(self, iterator):
                # the next 12 bytes are simply passed over, though they contain:
                # a record number: which doesn't seem to correspond to the dbf
                # a content length integer
                # a shapeType integer, which is never different form the shapeType of the file
                read = self.f.read(12)
                if read == '':
                        # signifies end of shapefile
                        return False
                else:
                    # get shapeType and creates appropriate feature
                    feature = classTypeDict[self.shapeType](self,iterator)
                    return feature
        
        ##################################################
        
        def addUserStrings(feature, geom):
            data = feature.dbfData
            for k in data:
                geom.SetUserString(k, str(data[k]))
            return geom
        
        def tVect(geom, vector):
            geom.Translate(vector)
            geom.SetUserString('TranslationVector', str(vector) )
            return geom
        
        def transVectorFromBBox(shpFile):
            """Uses the bounding box of a shapefile to make a vector moving Rhino geometry to the origin. The translation vector
            can also be stored as a user string the Rhino geometry, for later conversion back into geospatial data."""
            b = shpFile.boundingBox
            originalCenterPoint = ((b[0]+b[2])/2, (b[1]+b[3])/2, 0.0)
            translationVectr = Rhino.Geometry.Vector3d((b[0]+b[2])/-2.0, (b[1]+b[3])/-2.0, 0.0)
            return translationVectr
        
        def chop(indices, someList):
            for i in range(len(indices)-1):
                idx1, idx2 = indices[i], indices[i+1]
                yield someList[idx1:idx2]
        
        def chopPoints( feature ):
            if feature.numParts > 1:
                return [p for p in chop(feature.parts, feature.points3D)]
            else:
                return [feature.points3D]
        
        def shpToPoints( feature, translationVector=None ):
            # You can't set user strings to Point3d so for now lets skip it.
            #points = [addUserStrings(feature, Rhino.Geometry.Point3d(*p)) for p in feature.points3D]
            points = [Rhino.Geometry.Point3d(p[0],p[1],p[2]) for p in feature.points3D]
            if translationVector:
                points = [p.Add(p, translationVector) for p in points]
            return points
        
        def shpToCurve( feature, translationVector=None, degree=1):
            parts = chopPoints( feature )
            crvs = []
            for part in parts:
                points = []
                for pt in part:
                    rhPoint = Rhino.Geometry.Point3d( *pt )
                    points.append( rhPoint )
                crv = Rhino.Geometry.Curve.CreateControlPointCurve( points, degree )
                if translationVector:
                    crv = tVect(crv, translationVector )
                crvs.append( addUserStrings(feature, crv) )
            return crvs
        
        def shpToMesh( multiPatchFeature, translationVector=None ):
            m = multiPatchFeature
            parts = chopPoints(m)
            mesh = Rhino.Geometry.Mesh()
            for i, points in enumerate(parts):
                if m.partTypes[i] == 0: # it's a a triangle strip
                    submesh = Rhino.Geometry.Mesh()
                    for j, pt in enumerate(points): # build vertices
                        rhPoint = Rhino.Geometry.Point3d(*pt)
                        submesh.Vertices.Add(rhPoint)
                    for n in range(len(points)-1):
                        submesh.Faces.AddFace(n, n +1, n +2 )
                    submesh.Normals.ComputeNormals()
                    submesh.Compact()
                    mesh.Append(submesh)
                else: # it's some other geometry
                    return 'This geometry type is not yet supported, sorry.'
            mesh.UnifyNormals()
            mesh.Normals.ComputeNormals()
            mesh.Compact() # mesh all fresh and ready!
            if translationVector:
                mesh = tVect( mesh, translationVector)
            return [ addUserStrings(m, mesh) ]
        
        
        
        translationDict = {
                           'Point':shpToPoints,
                           'Polygon':shpToCurve,
                           'PolyLine':shpToCurve,
                           'PolyLineZ':shpToCurve,
                           'PolygonZ':shpToCurve,
                           'MultiPatch':shpToMesh
                           }
        
        def ShpFileToRhino( filepath, zero=True, tVect=None ):
            shpfile = ShpFile( filepath )
            if zero:
                tVect = transVectorFromBBox( shpfile )
            records = shpfile.records
            geoms = []
            for r in records:
                geoms.extend( translationDict[ shpfile.shapeType ]( r, tVect ) )
            return geoms
        
        ##################################################
        
        if read:
            if shapefile:
                if not os.path.exists(shapefile):
                    print 'The shapefile you gave me does not exist.\nDouble check the path: "%s"' % shapefile
                # import stuff
                out = ShpFileToRhino( shapefile, moveToCenter )
                print out
                geometry = out
            else:
                print 'no shapefile supplied'
        
        # return outputs if you have them; here I try it for you:
        return geometry
