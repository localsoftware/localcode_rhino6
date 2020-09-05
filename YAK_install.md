# Yak Installation Process


How to create the LocalCode plugin 
and install it with YAK

Tutorials:

From: "Tutorial: creating a Grasshopper component with the Python GHPY compiler"
By Giulio Piacentino, I used the second section, "2. Advanced compiling: multiple components, projects with modules, updating".

https://discourse.mcneel.com/t/tutorial-creating-a-grasshopper-component-with-the-python-ghpy-compiler/38552

From: "Step By Step
Creating a Grasshopper Plug-In Package
Creating a Rhino Plug-In Package
Pushing a Package to the Server
Installing and Managing Packages" 
I used all the sections. 

https://developer.rhino3d.com/guides/yak/

------------------

# Steps to compile the LocalCode plugin:
1. Compile the .ghpy file. 
2. Create the Yak file. 
3. Push to Yak server. 

------------------

## 1. Compile the .ghpy file:
To compile the plug-in:
* Write the python code in a GH Python component
* Go to 'Mode' tab and press 'Copy Compilable Code'
* Paste in a new GHPython Component 
* Export as python folder into a folder
* Do the same with the pytho code of all of the components

* Once you have all the Python files of the components
* Open a "Rhino Python Editor" window with the command 'EditPythonScript'
* Create a Python file called 'main.py' in the folder that contains all of your Python files
* This is the content of main, a first line with the name of the .ghpy file, 
Then a list of all the Python files for the components.

```
import clr

clr.CompileModules("LocalCode.ghpy",
                   "Bake_with_Attributes.py",
                   "Batch_Export.py",
                   "Batch_Import.py",
                   "Compare_GIS_Attributes.py",
                   "Create_View.py",
                   "Create_Pickle_View.py",
                   "Delete_All.py",
                   "Import_GeoJSON.py",
                   "Make_Material.py",
                   "Pickle_Data.py",
                   "Read_Shapefile.py",
                   "ShapeFile_Extract_User_Strings.py",
                   "UnPickle_Data.py",
                   "UnPickle_View.py",
                   "Write_SHP.py",
                   "Set_View.py"
                   )
```
        
* Run the code with the play button and you should get the .ghpy file.

# 2. Create the YAK file

* Create a folder with the following files:
