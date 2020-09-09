"""Deletes all geometries of Rhino document.

Deletes the Rhino geometry created by GH components.
This is useful for batch processing multiple files.

    Typical usage:
        Toggle a boolean in the 'Delete' input to erase the all the objects.


    Inputs:
        Delete: boolean delete

    Outputs:
        None"""

__author__ = "palomagr"
__version__ = "2020.07.09"

#ghenv.Component.Name = "Delete all"
#ghenv.Component.NickName = "Delete all"

from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class MyComponent(component):

    def RunScript(self, geom, Delete):
        bake = None
        def rcmd(commandstring, echo=True, mask=True):
            if mask:
                premask = '-_%s '
                try:
                    cmd = premask % commandstring
                except:
                    print commandstring, 'failed to mask'
            else:
                cmd = commandstring
            result = Rhino.RhinoApp.RunScript(cmd, echo)
            if not result:
                print 'The following command failed:'
                print ' ',cmd
            return result

        def rcmds(commands, echo=True, mask=True):
            for cmd in commands:
                rcmd( cmd, echo, mask )

        if Delete:
            rcmds(['SelAll','Delete'])
            #time.sleep(.5)
            delete = True


        else:
            bake = False

        # return outputs if you have them; here I try it for you:
        return
