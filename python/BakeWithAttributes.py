import Rhino

"""
Execute a single command from the Rhino command line.
"""
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

"""
Execute multiple commands in Rhino command line.
"""
def rcmds(commands, echo=True, mask=True):
    for cmd in commands:
        rcmd( cmd, echo, mask )


if Bake:
    delete = False
    
    if Delete:
        rcmds(['SelAll', 'Delete'])
        delete=True
    
    if delete:
        bake = True
        geom = geometry
        
    else:
        bake = True
        geom = geometry

else:
    bake = False
