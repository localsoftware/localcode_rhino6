import Rhino

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