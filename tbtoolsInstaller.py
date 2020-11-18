import pymel.core as pm
import os, stat
import sys
import inspect
import io
import shutil

class installer():
    filepath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\\"  # script directory
    iconPath = os.path.join(filepath, 'Icons')
    appPath = os.path.join(filepath, 'apps')

    def __init__(self):
        pass

    def install(self):
        print "[] RUNNING TBTOOLS INSTALLATION []"
        print self.filepath
        self.clearMultipleSysPaths()
        if self.filepath not in sys.path:
            sys.path.append(self.filepath)
        if self.iconPath not in sys.path:
            sys.path.append(self.iconPath)
        if self.appPath not in sys.path:
            sys.path.append(self.appPath)

        import module_startup
        module_startup.initialise().load_everything()

    def clearMultipleSysPaths(self):
        if self.filepath in sys.path:
            sys.path.remove(self.filepath)
        if self.iconPath in sys.path:
            sys.path.remove(self.iconPath)
        if self.appPath in sys.path:
            sys.path.remove(self.appPath)

    def install_no(self):
        result_message = "<h3>Installation result</h3>\t\n"
        if not self.write_module_file():
            result_message += "<span style=\""+self.colours['red']+"\">Failed to get access to module file</span>"

        if self.check_module_file():
            result_message += "module file created <span style=\""+self.colours['green']+ "\">Successfully</span> \n"
            result_message += "module file location <span style=\""+self.colours['yellow']+ "\">" \
                              + os.path.join(self.maya_module_dir, self.module_file) + "</span>\n\nEnjoy!"
            self.result_window()
        else:
            result_message += "<span style=\""+self.colours['red']+"<h3>WARNING</h3></span> :module file not created\n"

        message_state = pm.optionVar.get("inViewMessageEnable", 1)
        pm.optionVar(intValue=("inViewMessageEnable", 1))
        pm.inViewMessage(amg=result_message,
                         pos='botRight',
                         dragKill=True,
                         fadeOutTime=2.0,
                         fade=True)
        pm.optionVar(intValue=("inViewMessageEnable", message_state))

installer().install()
