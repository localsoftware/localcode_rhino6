List of working components:
* 1- BatchExport: compiled and locked
* 2- BatchImport: compiled and locked
* 3- CompareGISAttributes: compiled and locked
* 4- CreatePickleView: compiled and locked 
* 5- Createview: compiled and locked
* 6- ImportGeoJSON: compiled and locked 
* 7- PickleData: compiled and locked
* 8- ReadShapeFile: compiled and locked
* 9- SHPExtractUserString: compiled and locked
* 10- SetView: compiled and locked
* 11- UnPickleData: compiled and locked
* 12- WriteSHP: compiled and locked
* 13- Make Material
* 14- Bake with Attributes
* 15- Delete all
* 16- U pickle view

# Tasks Achieved:
* Tested original components
* Wrote descriptions 
* Developed bake + material
* Implemented Warnings Errors Remarks 
* Implemented YAK installation + documentation
* Fixed some of bugs  

## How to implement Runtime Messages: 

Usage example:

```
from Grasshopper.Kernel import GH_RuntimeMessageLevel as RML

        if geometry == None:
            self.AddRuntimeMessage(RML.Warning, "Add geometry in branches.")
```
The 'RML' can be a 'Warning', an 'Error', or a 'Remark'.
* The 'Remark' turns the component grey
* The 'Warning' turns the component orange. I wrote warnings for all the components, to inform the user they need to input data, whether it is geometry or other data types.
* The 'Error' turns the component red and it's used to signal wrong inputs.
