# localcode_rhino6

## TODO:
* Test BatchRender
* User test working components
* Fix broken components
* Make Installer Package [(Yak)](https://developer.rhino3d.com/guides/yak/what-is-yak/)

## Broken Components
* Select a Layer from geoJSON
* Bake With Attributes
* Write SHP

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
   
## Working Components without source code
* LayerFromDataTree
* DocLyrs
* SpatialJoin



