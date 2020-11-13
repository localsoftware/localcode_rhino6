# localcode_rhino6

## To Install from the windows command line:
`"C:\Program Files\Rhino 6\System\Yak.exe" install localcode`

or 

`"C:\Program Files\Rhino 7 WIP\System\Yak.exe" install localcode`


## TODO:
* Test BatchRender
* User test working components
* Make Installer Package [(Yak)](https://developer.rhino3d.com/guides/yak/what-is-yak/)

## Components to be Deleted
* LocalCodeImport (Must be deleted from GUI)
* LocalCodeExport (Must be deleted from GUI)
* UsrTxt
* DeleteAll

## Working Components with source code
* **BatchImport**  
   Compiled a working GHPY component. Source code and UserObject are updated.  
   In the past, there were errors saying an object had expired while running the component.  

* **BatchExport**  
   Compiled a working GHPY component. Source code and UserObject are updated.  
   Source code needs some work. The functions should not be nested within the RunScript function. But I found that the component broke when I unnested them. I was not able to figure out why. 

* **PickleData**  
   Compiled working GHPY component. Source code and UserObject are updated.  
   No errors in my tests.  

* **UnpickleData**  
   Compiled working GHPY component. Source code and UserObject are updated.  
   No errors in my tests.  

* **CreateView**  
   Compiled working GHPY component. Source code and UserObject are updated.  
   No errors in my tests.  

* **SetView**  
   Compiled working GHPY component. Source code and UserObject are updated.  
   No errors in my tests.  

* **CreatePickleView**  
   Compiled working GHPY component. Source code and UserObject are updated.  
   No errors in my tests.  

* **UnpickleView**  
   Compiled working GHPY component. Source code and UserObject are updated.  
   No errors in my tests.  

* **ImportGeoJSON**  
   Compiled working GHPY component. Source code and UserObject are updated.  
   No errors in my tests. Functions should be unnested from RunScript function, but are otherwise working.  
   
* **ReadShapefile**  
   Compiled working GHPY component. Source code and UserObject are updated.  
   No errors in my tests. Functions should be unnested from RunScript function, but are otherwise working.

* **SHPExtractUserStrings**  
   Compiled working GHPY component. Source code and UserObject are updated.  
   No errors in my tests. 

* **CompareGISAttributes**  
   Compiled working GHPY component. Source code and UserObject are updated.  
   No errors in my tests.  
   
* **Write SHP**  
   Compiled working GHPY component. Source code and UserObject are updated.  
   No errors in my tests.  
   
* **Bake With Attributes**  
   Working with preliminary tests. Likely used with BatchRender.  
   Large portion of code written in C#. Supporting function written in Python.  
   Source code archived. Component is not compiled as of now.  

   
## Working Components without source code
* **LayerFromDataTree**

* **DocLyrs**

* **SpatialJoin**

* **Select a Layer from geoJSON**  




