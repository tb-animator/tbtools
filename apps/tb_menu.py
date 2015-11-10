__author__ = 'Tom'
import maya.mel as mel
import pymel.core as pm
import webbrowser

class main_menu():
    def __init__(self):
        self.main_parent = ""
        self.main_menu = "TB_tools"


    def build_menu(self):
        self.main_parent = mel.eval('$tmpVar=$gMainWindow')
        pm.setParent(self.main_parent)
        if pm.menu(self.main_menu, exists=True):
            pm.deleteUI(self.main_menu)
        self.main_menu = pm.menu("TB_tools", label="TB_tools", tearOff=True)

        pm.menuItem(label="options",command=open_options, parent=self.main_menu)
        pm.menuItem(label="online help", command=open_anim_page, parent=self.main_menu)

def make_ui():
    main_menu().build_menu()


def open_options(*args):
    import tb_options as tbo
    reload(tbo)
    tbo.anim_optionWindow().showUI()

def open_anim_page(*args):
    webbrowser.open('http://tb-animator.blogspot.co.uk/')
