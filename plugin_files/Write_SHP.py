﻿from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython, System, Rhino
import rhinoscriptsyntax as rs
from struct import pack, unpack, calcsize, error
import os, time, array
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

class MyComponent(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "WriteSHP", "WriteSHP", """Write shapefile.py
Writes GH Geometries into ESRI Shapefiles.
based on the work of jlawhead<at>geospatialpython.com
	Typical usage:
Input geoemtry, projection and a boolean.""", "Extra", "LocalCode")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("701e57a0-ec50-4845-84d8-6e2d26234541")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Geometry()
        self.SetUpParam(p, "geometry", "geometry", "List of geometry objects to save in shapefile.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "fields", "fields", "List of attribute names for all geometry objects.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "values", "values", "Tree with attribute values for all geometry objects.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.tree
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "path", "path", "Path to destination file.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "filename", "filename", "destination file name.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "Activate", "Activate", "Boolean to write shapefile.")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "projection", "projection", "map projection to create PRJ file (required for readShapefile)")
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
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAHYcAAB2HAY/l8WUAAANZSURBVEhLvZV7SNNRFMc3p9OpbTNfezQ3t5Gm0zm1lq+0mc4yScXAIEsqUUpTMsrQnhBEFPSgsBTSUrQXRfVHZBEZFTESwpAsoj8qSEM0SMxHfTu7P5W0lpbSgQ/ce8+933PvOfd3f7z/bXOJECJ0hvgRv1jOyhTv7qpKPXZX6LB75z9A66qq9Fid6d9LegWcLGfC+BjJeyAZHJYZYF+/DOlp3l9IV8rJ83iSgvWqHiCVnEmzQCoqyrUjpBvIyfN44hWUHpttIWytpplDOrnZ/oOkq+bkuaP0EJhFhggNwUxMdBPjE4xhYpSUqKGQi1hfr/NE6AIxaweo3GEIEYPP52N5qh8yV8mwKFo6vnaUCSeYEEAX6IH+T4kY6LfgTXssBE58HNqvR3O9kfl3bdfiyoVwSCXOwAjlfNCe9xRsLlBNL8CeCi2uNYVDKBTgw6s4WBK9sb1UjbozBuYv36pBQ20oZP5CvH5uhq+PEMVFAWh/umh6AfZX6tByK5K1jWFzoNW4Y98uLWpPcQFKirgACrkQL2ycqFYtwss2M7X5rE84DhA83xP4Sumh3adafNjYjjIN+nqTSHAxuj4m4uSRIPj5uuBdZwyyqQaN9QY8uM1tahTHAexEGiVovR/NchuodkdJoQqdHTE4e0KPJ4+iUX0sGBKxM0b64oGhJPR0L0FC7NzpBaCPBAujuFtx43IEyuk2bSsOQPXxEDZWuEGFxtEavKIaKJUiiFwFY8JjOA7QTMdtquPy3VBrQNkWNREwocgXakIhlwnR8cyedyc2PgnHAcx0pzFsQZvNjOHPSZhHOzy4V4erjRHMX0UP2/VmI5QKV3S9jafb5vyz8Bh/rkFOpgyXLoYjK8Of9eNjpLAu4woeZRLTB+YDD3cB8tfK4eQ09QkkxADxu4kzQUswcyNuurgIkG6VoZSKuilfibxcBfLWTAOat3Gdkq3LylDAzY2lrJXwsouPm0AgsMaave6ePhGC7wP2tz2NmOr/YPdbgW/JOFdjQGKc9yN6ATJHJR1ailotunNgrx5d7+ieDy8FBui9mQyN93Ul4OjhIAQHzXlI66YUnmxWuVx0zxQhRUS45BdMJik0Ko/HNO+vhSdbGtFC/FxAu3AWMatmJc4T2aw3pfF4PwDYUPI/R5OVDQAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))


    def RunScript(self, geometry, fields, values, path, filename, Activate, projection):
        if geometry == None:
            self.AddRuntimeMessage(RML.Warning, "Add geometry in branches.")
        if path == None:
            self.AddRuntimeMessage(RML.Warning, "Add a path as a string.")
        if filename == None:
            self.AddRuntimeMessage(RML.Warning, "Add a filename as a string.")
        if Activate == None:
            self.AddRuntimeMessage(RML.Warning, "Add a boolean toggle for Activate.")
            
        import sys
        # Constants for shape types
        NULL = 0
        POINT = 1
        POLYLINE = 3
        POLYGON = 5
        MULTIPOINT = 8
        POINTZ = 11
        POLYLINEZ = 13
        POLYGONZ = 15
        MULTIPOINTZ = 18
        POINTM = 21
        POLYLINEM = 23
        POLYGONM = 25
        MULTIPOINTM = 28
        MULTIPATCH = 31

        PYTHON3 = sys.version_info[0] == 3

        def b(v):
            if PYTHON3:
                if isinstance(v, str):
                    # For python 3 encode str to bytes.
                    return v.encode('utf-8')
                elif isinstance(v, bytes):
                    # Already bytes.
                    return v
                else:
                    # Error.
                    raise Exception('Unknown input type')
                    #self.AddRuntimeMessage(RML.Warning,'Unknown input type')
            else:
                # For python 2 assume str passed in and return str.
                return v

        def u(v):
            if PYTHON3:
                if isinstance(v, bytes):
                    # For python 3 decode bytes to str.
                    return v.decode('utf-8')
                elif isinstance(v, str):
                    # Already str.
                    return v
                else:
                    # Error.
                    raise Exception('Unknown input type')
            else:
                # For python 2 assume str passed in and return str.
                return v

        def is_string(v):
            if PYTHON3:
                return isinstance(v, str)
            else:
                return isinstance(v, basestring)

        class _Array(array.array):
            """Converts python tuples to lits of the appropritate type.
            Used to unpack different shapefile header parts."""
            def __repr__(self):
                return str(self.tolist())

        class _Shape:
            def __init__(self, shapeType=None):
                """Stores the geometry of the different shape types
                specified in the Shapefile spec. Shape types are
                usually point, polyline, or polygons. Every shape type
                except the "Null" type contains points at some level for
                example verticies in a polygon. If a shape type has
                multiple shapes containing points within a single
                geometry record then those shapes are called parts. Parts
                are designated by their starting index in geometry record's
                list of shapes."""
                self.shapeType = shapeType
                self.points = []

        class _ShapeRecord:
            """A shape object of any type."""
            def __init__(self, shape=None, record=None):
                self.shape = shape
                self.record = record

        class ShapefileException(Exception):
            """An exception to handle shapefile specific problems."""
            pass

        class Writer:
            """Provides write support for ESRI Shapefiles."""
            def __init__(self, shapeType=None):
                self._shapes = []
                self.fields = []
                self.records = []
                self.shapeType = shapeType
                self.shp = None
                self.shx = None
                self.dbf = None
                # Geometry record offsets and lengths for writing shx file.
                self._offsets = []
                self._lengths = []
                # Use deletion flags in dbf? Default is false (0).
                self.deletionFlag = 0

            def __getFileObj(self, f):
                """Safety handler to verify file-like objects"""
                if not f:
                    raise ShapefileException("No file-like object available.")
                elif hasattr(f, "write"):
                    return f
                else:
                    pth = os.path.split(f)[0]
                    if pth and not os.path.exists(pth):
                        os.makedirs(pth)
                    return open(f, "wb")

            def __shpFileLength(self):
                """Calculates the file length of the shp file."""
                # Start with header length
                size = 100
                # Calculate size of all shapes
                for s in self._shapes:
                    # Add in record header and shape type fields
                    size += 12
                    # nParts and nPoints do not apply to all shapes
                    #if self.shapeType not in (0,1):
                    #       nParts = len(s.parts)
                    #       nPoints = len(s.points)
                    if hasattr(s,'parts'):
                        nParts = len(s.parts)
                    if hasattr(s,'points'):
                        nPoints = len(s.points)
                    # All shape types capable of having a bounding box
                    if self.shapeType in (3,5,8,13,15,18,23,25,28,31):
                        size += 32
                    # Shape types with parts
                    if self.shapeType in (3,5,13,15,23,25,31):
                        # Parts count
                        size += 4
                        # Parts index array
                        size += nParts * 4
                    # Shape types with points
                    if self.shapeType in (3,5,8,13,15,23,25,31):
                        # Points count
                        size += 4
                        # Points array
                        size += 16 * nPoints
                    # Calc size of part types for Multipatch (31)
                    if self.shapeType == 31:
                        size += nParts * 4
                    # Calc z extremes and values
                    if self.shapeType in (13,15,18,31):
                        # z extremes
                        size += 16
                        # z array
                        size += 8 * nPoints
                    # Calc m extremes and values
                    if self.shapeType in (23,25,31):
                        # m extremes
                        size += 16
                        # m array
                        size += 8 * nPoints
                    # Calc a single point
                    if self.shapeType in (1,11,21):
                        size += 16
                    # Calc a single Z value
                    if self.shapeType == 11:
                        size += 8
                    # Calc a single M value
                    if self.shapeType in (11,21):
                        size += 8
                # Calculate size as 16-bit words
                size //= 2
                return size

            def __bbox(self, shapes, shapeTypes=[]):
                x = []
                y = []
                for s in shapes:
                    shapeType = self.shapeType
                    if shapeTypes:
                        shapeType = shapeTypes[shapes.index(s)]
                    px, py = list(zip(*s.points))[:2]
                    x.extend(px)
                    y.extend(py)
                return [min(x), min(y), max(x), max(y)]

            def __zbox(self, shapes, shapeTypes=[]):
                z = []
                for s in shapes:
                    try:
                        for p in s.points:
                            z.append(p[2])
                    except IndexError:
                        pass
                if not z: z.append(0)
                return [min(z), max(z)]

            def __mbox(self, shapes, shapeTypes=[]):
                m = [0]
                for s in shapes:
                    try:
                        for p in s.points:
                            m.append(p[3])
                    except IndexError:
                        pass
                return [min(m), max(m)]

            def bbox(self):
                """Returns the current bounding box for the shapefile which is
                the lower-left and upper-right corners. It does not contain the
                elevation or measure extremes."""
                return self.__bbox(self._shapes)

            def zbox(self):
                """Returns the current z extremes for the shapefile."""
                return self.__zbox(self._shapes)

            def mbox(self):
                """Returns the current m extremes for the shapefile."""
                return self.__mbox(self._shapes)

            def __shapefileHeader(self, fileObj, headerType='shp'):
                """Writes the specified header type to the specified file-like object.
                Several of the shapefile formats are so similar that a single generic
                method to read or write them is warranted."""
                f = self.__getFileObj(fileObj)
                f.seek(0)
                # File code, Unused bytes
                f.write(pack(">6i", 9994,0,0,0,0,0))
                # File length (Bytes / 2 = 16-bit words)
                if headerType == 'shp':
                    f.write(pack(">i", self.__shpFileLength()))
                elif headerType == 'shx':
                    f.write(pack('>i', ((100 + (len(self._shapes) * 8)) // 2)))
                # Version, Shape type
                f.write(pack("<2i", 1000, self.shapeType))
                # The shapefile's bounding box (lower left, upper right)
                if self.shapeType != 0:
                    try:
                        f.write(pack("<4d", *self.bbox()))
                    except error:
                        raise ShapefileException("Failed to write shapefile bounding box. Floats required.")
                else:
                    f.write(pack("<4d", 0,0,0,0))
                # Elevation
                z = self.zbox()
                # Measure
                m = self.mbox()
                try:
                    f.write(pack("<4d", z[0], z[1], m[0], m[1]))
                except error:
                    raise ShapefileException("Failed to write shapefile elevation and measure values. Floats required.")

            def __dbfHeader(self):
                """Writes the dbf header and field descriptors."""
                f = self.__getFileObj(self.dbf)
                f.seek(0)
                version = 3
                year, month, day = time.localtime()[:3]
                year -= 1900
                # Remove deletion flag placeholder from fields
                for field in self.fields:
                    if field[0].startswith("Deletion"):
                        self.fields.remove(field)
                numRecs = len(self.records)
                numFields = len(self.fields)
                headerLength = numFields * 32 + 33
                recordLength = sum([int(field[2]) for field in self.fields]) + 1
                header = pack('<BBBBLHH20x', version, year, month, day, numRecs,
                        headerLength, recordLength)
                f.write(header)
                # Field descriptors
                for field in self.fields:
                    name, fieldType, size, decimal = field
                    name = b(name)
                    name = name.replace(b(' '), b('_'))
                    name = name.ljust(11).replace(b(' '), b('\x00'))
                    fieldType = b(fieldType)
                    size = int(size)
                    fld = pack('<11sc4xBB14x', name, fieldType, size, decimal)
                    f.write(fld)
                # Terminator
                f.write(b('\r'))

            def __shpRecords(self):
                """Write the shp records"""
                f = self.__getFileObj(self.shp)
                f.seek(100)
                recNum = 1
                for s in self._shapes:
                    self._offsets.append(f.tell())
                    # Record number, Content length place holder
                    f.write(pack(">2i", recNum, 0))
                    recNum += 1
                    start = f.tell()
                    # Shape Type
                    f.write(pack("<i", s.shapeType))
                    # All shape types capable of having a bounding box
                    if s.shapeType in (3,5,8,13,15,18,23,25,28,31):
                        try:
                            f.write(pack("<4d", *self.__bbox([s])))
                        except error:
                            raise ShapefileException("Falied to write bounding box for record %s. Expected floats." % recNum)
                    # Shape types with parts
                    if s.shapeType in (3,5,13,15,23,25,31):
                        # Number of parts
                        f.write(pack("<i", len(s.parts)))
                    # Shape types with multiple points per record
                    if s.shapeType in (3,5,8,13,15,23,25,31):
                        # Number of points
                        f.write(pack("<i", len(s.points)))
                    # Write part indexes
                    if s.shapeType in (3,5,13,15,23,25,31):
                        for p in s.parts:
                            f.write(pack("<i", p))
                    # Part types for Multipatch (31)
                    if s.shapeType == 31:
                        for pt in s.partTypes:
                            f.write(pack("<i", pt))
                    # Write points for multiple-point records
                    if s.shapeType in (3,5,8,13,15,23,25,31):
                        try:
                            [f.write(pack("<2d", *p[:2])) for p in s.points]
                        except error:
                            raise ShapefileException("Failed to write points for record %s. Expected floats." % recNum)
                    # Write z extremes and values
                    if s.shapeType in (13,15,18,31):
                        try:
                            f.write(pack("<2d", *self.__zbox([s])))
                        except error:
                            raise ShapefileException("Failed to write elevation extremes for record %s. Expected floats." % recNum)
                        try:
                            [f.write(pack("<d", p[2])) for p in s.points]
                        except error:
                            raise ShapefileException("Failed to write elevation values for record %s. Expected floats." % recNum)
                    # Write m extremes and values
                    if s.shapeType in (23,25,31):
                        try:
                            f.write(pack("<2d", *self.__mbox([s])))
                        except error:
                            raise ShapefileException("Failed to write measure extremes for record %s. Expected floats" % recNum)
                        try:
                            [f.write(pack("<d", p[3])) for p in s.points]
                        except error:
                            raise ShapefileException("Failed to write measure values for record %s. Expected floats" % recNum)
                    # Write a single point
                    if s.shapeType in (1,11,21):
                        try:
                            f.write(pack("<2d", s.points[0][0], s.points[0][1]))
                        except error:
                            raise ShapefileException("Failed to write point for record %s. Expected floats." % recNum)
                    # Write a single Z value
                    if s.shapeType == 11:
                        try:
                            f.write(pack("<1d", s.points[0][2]))
                        except error:
                            raise ShapefileException("Failed to write elevation value for record %s. Expected floats." % recNum)
                    # Write a single M value
                    if s.shapeType in (11,21):
                        try:
                            f.write(pack("<1d", s.points[0][3]))
                        except error:
                            raise ShapefileException("Failed to write measure value for record %s. Expected floats." % recNum)
                    # Finalize record length as 16-bit words
                    finish = f.tell()
                    length = (finish - start) // 2
                    self._lengths.append(length)
                    # start - 4 bytes is the content length field
                    f.seek(start-4)
                    f.write(pack(">i", length))
                    f.seek(finish)

            def __shxRecords(self):
                """Writes the shx records."""
                f = self.__getFileObj(self.shx)
                f.seek(100)
                for i in range(len(self._shapes)):
                    f.write(pack(">i", self._offsets[i] // 2))
                    f.write(pack(">i", self._lengths[i]))

            def __dbfRecords(self):
                """Writes the dbf records."""
                f = self.__getFileObj(self.dbf)
                for record in self.records:
                    if not self.fields[0][0].startswith("Deletion"):
                        f.write(b(' ')) # deletion flag
                    for (fieldName, fieldType, size, dec), value in zip(self.fields, record):
                        fieldType = fieldType.upper()
                        size = int(size)
                        if fieldType.upper() == "N":
                            value = str(value).rjust(size)
                        elif fieldType == 'L':
                            value = str(value)[0].upper()
                        else:
                            value = str(value)[:size].ljust(size)
                        assert len(value) == size
                        value = b(value)
                        f.write(value)

            def null(self):
                """Creates a null shape."""
                self._shapes.append(_Shape(NULL))

            def point(self, x, y, z=0, m=0):
                """Creates a point shape."""
                pointShape = _Shape(self.shapeType)
                pointShape.points.append([x, y, z, m])
                self._shapes.append(pointShape)

            def line(self, parts=[], shapeType=POLYLINE):
                """Creates a line shape. This method is just a convienience method
                which wraps 'poly()'.
                """
                self.poly(parts, shapeType, [])

            def poly(self, parts=[], shapeType=POLYGON, partTypes=[]):
                """Creates a shape that has multiple collections of points (parts)
                including lines, polygons, and even multipoint shapes. If no shape type
                is specified it defaults to 'polygon'. If no part types are specified
                (which they normally won't be) then all parts default to the shape type.
                """
                polyShape = _Shape(shapeType)
                polyShape.parts = []
                polyShape.points = []
                for part in parts:
                    polyShape.parts.append(len(polyShape.points))
                    for point in part:
                        # Ensure point is list
                        if not isinstance(point, list):
                            point = list(point)
                        # Make sure point has z and m values
                        while len(point) < 4:
                            point.append(0)
                        polyShape.points.append(point)
                if polyShape.shapeType == 31:
                    if not partTypes:
                        for part in parts:
                            partTypes.append(polyShape.shapeType)
                    polyShape.partTypes = partTypes
                self._shapes.append(polyShape)

            def field(self, name, fieldType="C", size="50", decimal=0):
                """Adds a dbf field descriptor to the shapefile."""
                self.fields.append((name, fieldType, size, decimal))

            def record(self, *recordList, **recordDict):
                """Creates a dbf attribute record. You can submit either a sequence of
                field values or keyword arguments of field names and values. Before
                adding records you must add fields for the record values using the
                fields() method. If the record values exceed the number of fields the
                extra ones won't be added. In the case of using keyword arguments to specify
                field/value pairs only fields matching the already registered fields
                will be added."""
                record = []
                fieldCount = len(self.fields)
                # Compensate for deletion flag
                if self.fields[0][0].startswith("Deletion"): fieldCount -= 1
                if recordList:
                    [record.append(recordList[i]) for i in range(fieldCount)]
                elif recordDict:
                    for field in self.fields:
                        if field[0] in recordDict:
                            val = recordDict[field[0]]
                            if val:
                                record.append(val)
                            else:
                                record.append("")
                if record:
                    self.records.append(record)

            def shape(self, i):
                return self._shapes[i]

            def shapes(self):
                """Return the current list of shapes."""
                return self._shapes

            def saveShp(self, target):
                """Save an shp file."""
                if not hasattr(target, "write"):
                    target = os.path.splitext(target)[0] + '.shp'
                if not self.shapeType:
                    self.shapeType = self._shapes[0].shapeType
                self.shp = self.__getFileObj(target)
                self.__shapefileHeader(self.shp, headerType='shp')
                self.__shpRecords()

            def saveShx(self, target):
                """Save an shx file."""
                if not hasattr(target, "write"):
                    target = os.path.splitext(target)[0] + '.shx'
                if not self.shapeType:
                    self.shapeType = self._shapes[0].shapeType
                self.shx = self.__getFileObj(target)
                self.__shapefileHeader(self.shx, headerType='shx')
                self.__shxRecords()

            def saveDbf(self, target):
                """Save a dbf file."""
                if not hasattr(target, "write"):
                    target = os.path.splitext(target)[0] + '.dbf'
                self.dbf = self.__getFileObj(target)
                self.__dbfHeader()
                self.__dbfRecords()

            def save(self, target=None, shp=None, shx=None, dbf=None):
                """Save the shapefile data to three files or
                three file-like objects. SHP and DBF files can also
                be written exclusively using saveShp, saveShx, and saveDbf respectively."""
                # TODO: Create a unique filename for target if None.
                if shp:
                    self.saveShp(shp)
                if shx:
                    self.saveShx(shx)
                if dbf:
                    self.saveDbf(dbf)
                elif target:
                    self.saveShp(target)
                    self.shp.close()
                    self.saveShx(target)
                    self.shx.close()
                    self.saveDbf(target)
                    self.dbf.close()

        def Main():
            if path!=None and filename!=None:
                file = os.path.join(path, filename)
                if Activate == True:
                    if type(geometry[0]) == Rhino.Geometry.Point: # If it is a point collection
                        w = Writer(POINT)
                        for field in fields: # Write the fields in the dbf
                            w.field(field)
                        for i, pt in enumerate(geometry):
                            vals = get_fields(i, fields, values, geometry)
                            point = rs.PointCoordinates(pt) # Turn the points into Rhino pt objects
                            w.point(point.X, point.Y, point.Z) # Write the pts as shp geometry objects
                            w.record(*vals) # Write the values for each pt
                        w.save(file)

                    else:
                        if geometry[0].IsClosed == False: # If the geometry is a curve, write a line shp
                            w = Writer(POLYLINE)
                            for field in fields: # Write the fields in the dbf
                                w.field(field)
                            for i, crv in enumerate(geometry):
                                cp = rs.CurvePoints(crv) # get the cps of the curves
                                if len(cp) >1: # Make sure it's a line
                                    vals = get_fields(i, fields, values, geometry)
                                    points = [[[pt.X,pt.Y,pt.Z] for pt in cp]] # create a formated nested list from the cps to write the shp
                                    w.poly(parts=points) # Write the polylines as shp geometry objects
                                    w.record(*vals) # Write the values for each pt
                            w.save(file)

                        else: # It is a polygon
                            w = Writer(POLYGON)
                            for field in fields: # Write the fields in the dbf
                                w.field(field)
                            for i, crv in enumerate(geometry):
                                cp = rs.CurvePoints(crv) # get the cps of the curves
                                if len(cp) >1: # Make sure it's a line
                                    vals = get_fields(i, fields, values, geometry)
                                    points = [[[pt.X,pt.Y,pt.Z] for pt in cp]] # create a formated nested list from the cps to write the shp
                                    w.poly(parts=points) # Write the polylines as shp geometry objects
                                    w.record(*vals) # Write the values for each pt
                            w.save(file)
                if projection:
                    prj(file, projection)

        def get_fields(i, fields, values, geometry):
            vals = [] # Create a list to store values for each geom
            for h in range(len(fields)):
                vals.append(values[values.Path(i),h]) # I iterate through the data tree and build individual lists
            return vals

        def prj(file, epsg):
            # create the PRJ file
            prj = open("%s.prj" % file, "w")
            prj.write(epsg)
            prj.close()

#        if __name__ == "__main__":
#            Main()

        Main()

        # return outputs if you have them; here I try it for you:
        return


import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "WriteSHP"
    
    def get_AssemblyDescription(self):
        return """"""

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("b875e944-5e55-49fc-bb5b-536a4204b856")