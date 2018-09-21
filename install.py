import pymel.core as pm
import os, stat
import sys
import inspect
import io
import shutil

class module_maker():
    def __init__(self):
        self.colours = {'red': "color:#F05A5A;",
                        'green': "color:#82C99A;",
                        'yellow': "color:#F4FA58;"
                        }
        self.win_versions = ['win32', 'win64'][pm.about(is64=True)]
        self.maya_version = pm.about(version=True)
        self.filepath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) +"\\"  # script directory
        self.python_paths = ['apps', 'lib', '']
        self.maya_script_paths = ['scripts']
        self.xbmlang_paths = ['Icons']
        self.out_lines = []
        self.module_file = 'tbtools.mod'
        self.module_template = os.path.join(self.filepath, self.module_file)
        self.maya_module_dir = pm.internalVar(userAppDir=True) + "modules\\"
        if not os.path.isdir(self.maya_module_dir):
            print "making maya module folder"
            os.mkdir(self.maya_module_dir)
        else:
            os.chmod(self.maya_module_dir, stat.S_IWRITE)
        self.current_module_data = None
        self.module_path = os.path.join(self.maya_module_dir, self.module_file)

    def make_module_path(self):
        module_path = '+ PLATFORM:' \
                      + self.win_versions \
                      + ' MAYAVERSION:' \
                      + self.maya_version \
                      + ' tbtools 1.0 ' \
                      + self.filepath + '\\'
        return module_path

    def make_module_data(self):
        self.out_lines = ['\n']
        self.out_lines.append(self.make_module_path())
        for paths in self.python_paths:
            self.out_lines.append('PYTHONPATH+:='+paths)
        for paths in self.maya_script_paths:
            self.out_lines.append('MAYA_SCRIPT_PATH+:='+paths)
        for paths in self.xbmlang_paths:
            self.out_lines.append('XBMLANGPATH+:='+paths)

    def write_module_file(self):
        self.read_module_file()
        mod_file = self.maya_module_dir + "\\" + self.module_file
        shutil.copyfile(self.module_template, mod_file)

        if os.access(os.path.join(self.maya_module_dir, self.module_file), os.W_OK):
            with io.open(mod_file, 'w') as f:
                f.writelines(line + u'\n' for line in self.current_module_data)
                return True
        else:
            return False

    def read_module_file(self):
        print 'read_module_file'
        if os.path.isfile(self.module_path):
            f = open(self.module_path, 'r')
            self.current_module_data = f.read().splitlines()
            match = False
            f.close()
            for lineIndex, line in enumerate(self.current_module_data):
                if 'PLATFORM:%s' % self.win_versions  and 'MAYAVERSION:%s' % self.maya_version in line:
                    match = True
                    self.current_module_data[lineIndex] = self.make_module_path()
            if not match:
                # create a new entry
                print 'making new entry'
                self.make_module_data()
                print 'current_module_data', self.current_module_data
                self.current_module_data.extend(self.out_lines)

    def replace_path(self, fileName, path, newpath):
        f = open(fileName,'r')
        filedata = f.read()
        f.close()

        newdata = filedata.replace(path, newpath)

        f = open(fileName, 'w')
        f.write(newdata)
        f.close()

    def check_module_file(self):
        full_path = os.path.join(self.maya_module_dir, self.module_file)
        print full_path
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

    def result_window(self):
        if pm.window("installWin", exists=True):
            pm.deleteUI("installWin")
        window = pm.window( title="success!")
        layout = pm.columnLayout(adjustableColumn=True )
        pm.text(font="boldLabelFont",label="tbtools installed")
        pm.text(label="")
        pm.text(label="please restart maya for everything to load")

        pm.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)'), parent=layout)
        pm.setParent('..')
        pm.showWindow(window)

module_maker().install()
