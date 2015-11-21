__author__ = 'tom.bailey'
'''TB Animation Tools is a toolset for animators

*******************************************************************************
    License and Copyright
    Copyright 2015-Tom Bailey
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    this script holds a bunch of useful timeline functions to make life easier

    send issues/ requests to brimblashman@gmail.com
    visit tb-animator.blogspot.com for "stuff"

*******************************************************************************
'''
import pymel.core as pm
import maya.cmds as mc
import os.path
from tb_timeline import timeline

def make_playblast(type="mov"):
    formats = { "mov": "qt", "avi": "avi" }
    my_timeline = timeline()
    directory = pm.optionVar.get('tb_playblast_folder', 'c://qss//')
    file = mc.file(query=True, sceneName=True, shortName=True)
    filename = file.split('.')[0]

    folderName = '%sp_%s/' % (directory, filename)
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    count = len(mc.getFileList(fld=folderName))
    string_count = len(str(count))
    string_base = "0000"
    string_base_count = len(string_base)
    index = string_base_count-string_count
    string_result = string_base[:index]
    blast_name = '%s%s_%s%s.%s' % (folderName,filename,string_result,count,type)

    if my_timeline.isHighlighted():
        __range = my_timeline.get_highlighted_range()
    else:
        __range = my_timeline.get_range()
    print "pb range", __range
    print "file name to save", blast_name
    mc.playblast(startTime=__range[0], endTime=__range[1], format=formats[type],
        clearCache=False, percent=75, filename=blast_name)

