import pymel.core as pm
import os
import sys
import inspect
import io

class module_maker():
    def __init__(self):
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
        with io.open(file, 'w') as f:
            f.writelines(line + u'\n' for line in self.out_lines)

module_maker().write_module_file()