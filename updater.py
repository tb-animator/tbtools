__author__ = 'Tom'
import pickle
import urllib2
import os
import pymel.core as pm

import project_data as prj
reload(prj)

class updater():
    def __init__(self):
        self.master_url = 'https://raw.githubusercontent.com/tb-animator/tbtools/master/'
        self.realPath = os.path.realpath(__file__)
        self.basename = os.path.basename(__file__)
        self.base_dir = os.path.normpath(os.path.dirname(__file__))
        self.data_file = "prj_files.poo"
        self.out_files = []
        self.version = pm.optionVar.get('tb_version', 1.0 )
        self.project_info = self.load_project_data_from_git()

    def check_version(self):
        if self.project_info.version > self.version:
            updaterWindow().showUI()
            print "where's the window"


    def get_url_dir(self, dir):
        print "in", dir
        print self.base_dir
        out = dir.replace(self.base_dir,self.master_url).replace("\\","/")
        return out


    def load_project_data(self):
        data = pickle.load(open(os.path.join(self.base_dir,self.data_file), "rb" ))
        return data


    def load_project_data_from_git(self):
        url = self.master_url + self.data_file
        print url
        data = pickle.load(urllib2.urlopen(url, "rb"))
        return data


    def create_url(self, item):
        url = (self.master_url + item).replace("\\","/")
        return url


    def read_from_url(self, url):
        lines = []
        data = urllib2.urlopen(url)
        for line in data:
            lines.append(line)
        return lines


    def copy_from_url(self, url, fileName):
        if fileName:
            dirName = os.path.split(fileName)[0]
            if not os.path.isdir(dirName):
                print "making folder", dirName
                os.mkdir(dirName)
            '''
            # read the target script from git
            01file_data = self.read_from_url(url)
            print "downloading:: ", fileName
            if file_data:
                # nukes the current file
                f = open(fileName,"w")
            
                # writes into the file from the url
                f.writelines(file_data)
                f.close()
            '''
            print "dowloading file:", fileName
            remote_file = urllib2.urlopen(url)
            localFile = open(fileName, 'wb')
            localFile.write(remote_file.read())
            localFile.close()
        else:
            print "no fileName"
        
            
    def download_project_files(self):
        files = self.project_info.scripts
        print "downloading module to ", self.base_dir
        for fileName in files:
            # print self.base_dir, fileName
            local_dir = '%s\%s' % (self.base_dir,fileName)
            url = self.create_url(fileName)
            # print "local", local_dir, "url", url
            try:
                self.copy_from_url(url, local_dir)
            except:
                print "skipping", url

class updaterWindow():
    def __init__(self):
        self.project_data = updater().project_info

    def showUI(self):
        window = pm.window( title="tb tools update")
        layout = pm.columnLayout(adjustableColumn=True )
        pm.text(font="boldLabelFont",label="There's a new version")
        pm.text(label=self.project_data.version)
        pm.text(label="release notes")
        pm.scrollField( editable=True, wordWrap=False, text=self.project_data.relaseNotes )
        '''
        for items in self.command_list:
            self.command_widget(command_name=items, parent=layout)
        '''

        # pm.button( label='Delete all', parent=layout)
        pm.button( label='Update', command=updater().download_project_files , parent=layout)
        pm.button( label='Ignore this version', command=('cmds.deleteUI(\"' + window + '\", window=True)') , parent=layout)
        pm.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') , parent=layout)
        pm.setParent( '..' )
        pm.showWindow(window)