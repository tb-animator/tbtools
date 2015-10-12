import pymel.core as pm
import os, stat
import sys
import inspect
import io

class module_maker():
    def __init__(self):
        self.colours = {'red': "color:#F05A5A;",
                        'green': "color:#82C99A;",
                        'yellow': "color:#F4FA58;"
                        }
        self.win_versions = ['win32', 'win64'][pm.about(is64=True)]
        self.maya_version = pm.about(version=True)
        self.filepath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  # script directory
        self.python_paths = ['apps', 'lib', '']
        self.maya_script_paths = ['scripts']
        self.xbmlang_paths = ['Icons']
        self.out_lines = []
        self.module_file = 'tbtools.mod'
        self.maya_module_dir = pm.internalVar(userAppDir=True) + "modules\\"
        if not os.path.isdir(self.maya_module_dir):
            print "making maya module folder"
            os.mkdir(self.maya_module_dir)
        else:
            os.chmod(self.maya_module_dir, stat.S_IWRITE)

    def make_module_path(self):
        module_path = '+ PLATFORM:' \
               + self.win_versions \
               + ' MAYAVERSION:' \
               + self.maya_version \
               + ' tbtools 1.0 ' \
               + self.filepath + '\\'
        return module_path

    def make_module_data(self):
        self.out_lines.append(self.make_module_path())
        for paths in self.python_paths:
            self.out_lines.append('PYTHONPATH+:='+paths)
        for paths in self.maya_script_paths:
            self.out_lines.append('MAYA_SCRIPT_PATH+:='+paths)
        for paths in self.xbmlang_paths:
            self.out_lines.append('XBMLANGPATH+:='+paths)


    def write_module_file(self):
        self.make_module_data()
        file = self.maya_module_dir + "\\" + self.module_file
        if os.access(os.path.join(self.maya_module_dir, self.module_file), os.W_OK):
            with io.open(file, 'w') as f:
                f.writelines(line + u'\n' for line in self.out_lines)
                return True
        else:
            return False

    def check_module_file(self):
        full_path = os.path.join(self.maya_module_dir, self.module_file)
        if os.path.isfile(os.path.join(self.maya_module_dir, self.module_file)):
            os.chmod(full_path, stat.S_IWRITE)
            return True
        else:
            return False

    def install(self):
        result_message = "<h3>Installation result</h3>\t\n"
        if not self.write_module_file():
            result_message += "<span style=\""+self.colours['red']+"\">Failed to get access to module file</span>"

        if self.check_module_file():
            result_message += "module file created <span style=\""+self.colours['green']+ "\">Successfully</span> \n"
            result_message += "module file location <span style=\""+self.colours['yellow']+ "\">" \
                              + os.path.join(self.maya_module_dir, self.module_file) + "</span>\n\nEnjoy!"
        else:
            result_message += "<span style=\""+self.colours['red']+"<h3>WARNING</h3></span> :module file not created\n"
        pm.inViewMessage(amg=result_message,
                 pos='midCenter',
                 dragKill=True,
                 fadeOutTime=2.0,
                 fade=True)

module_maker().install()