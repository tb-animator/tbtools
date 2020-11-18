import pymel.core as pm
import os
import sys
import inspect


class installer():
    filepath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\\"  # script directory
    iconPath = os.path.join(filepath, 'Icons')
    appPath = os.path.join(filepath, 'apps')
    colours = {'red': "color:#F05A5A;",
               'green': "color:#82C99A;",
               'yellow': "color:#F4FA58;"
               }

    def __init__(self):
        pass

    def install(self):
        print "[] RUNNING TBTOOLS INSTALLATION []"
        print self.filepath

        try:
            self.clearMultipleSysPaths()
            if self.filepath not in sys.path:
                sys.path.append(self.filepath)
            if self.iconPath not in sys.path:
                sys.path.append(self.iconPath)
            if self.appPath not in sys.path:
                sys.path.append(self.appPath)

            import module_startup
            module_startup.initialise().load_everything()
            import tb_messages
            tb_messages.info(prefix=' INSTALLATION',
                             message=' : Success',
                             fadeStayTime=5,
                             fadeOutTime=5,
                             fade=True,
                             position='botRight')
        except:
            pm.warning('installation failed')

    def clearMultipleSysPaths(self):
        if self.filepath in sys.path:
            sys.path.remove(self.filepath)
        if self.iconPath in sys.path:
            sys.path.remove(self.iconPath)
        if self.appPath in sys.path:
            sys.path.remove(self.appPath)

    def result_window(self):
        if pm.window("installWin", exists=True):
            pm.deleteUI("installWin")
        window = pm.window(title="success!")
        layout = pm.columnLayout(adjustableColumn=True)
        pm.text(font="boldLabelFont", label="tbtools installed")
        pm.text(label="")
        pm.button(label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)'), parent=layout)
        pm.setParent('..')
        pm.showWindow(window)


installer().install()
