
import pymel.core as pm
import fnmatch

def track(*args):
    return trackingCamera.DoIt(args)


class trackingCamera(object):
    @classmethod
    def DoIt(cls, *args):
        """A function """
        check_nodes()
        trck = cls()

        # lambda *args: checkBox_pressed(_name, args[0])
        print args[0], " args"
        _message = ''
        out_message = ''
        if args:
            for arg in args[0]:
                __dict = {"retarget": trck.retarget,
                          "persp": trck.swap_view,
                          "tracker": trck.swap_view
                          }
                _message = __dict[arg](arg)

                out_message = out_message + _message
                print "success"
        if out_message:
            pm.inViewMessage(amg=out_message,
                          pos='botLeft',
                          fadeStayTime=len(out_message)*60.0,
                          fadeOutTime=100.0,
                          fade=True)

        return trck

    def __init__(self):
        print "init start"
        self.camera_target = pm.ls(selection=True)
        if self.camera_target:
            self.camera_target = self.camera_target[0]
        self._cameras = []
        self.cam_list = pm.ls(cameras=True)
        self.currentView = pm.lookThru(query=True)
        self._cameras.append([pm.listTransforms(fnmatch.filter(self.cam_list, '*persp*'))[0]])
        # any camera called tracker?
        _tracker = pm.listTransforms(fnmatch.filter(self.cam_list, '*tracker*'))
        if _tracker:
            self._cameras.append([pm.listTransforms(fnmatch.filter(self.cam_list, '*tracker*'))[0]])
            self.tracker_grp = pm.listRelatives(self._cameras[1], parent=True)
        else:
            # no tracking camera found
            self.tracker_cam = pm.camera(name='tracker_cam')
            self.tracker_grp = pm.group(empty=True, world=True, name="tracker_grp")
            print "parenting ", self.tracker_cam[0], "to", self.tracker_grp
            pm.parent(self.tracker_cam[0], self.tracker_grp)
            self._cameras.append(self.tracker_cam)

        self.current_t = pm.xform(self.currentView, query=True, worldSpace=True, absolute=True, translation=True)
        self.current_r = pm.xform(self.currentView, query=True, absolute=True, rotation=True)

        self.constraint = pm.listRelatives(self.tracker_grp, type='pointConstraint')
        if not self.constraint:
            # constraint list is empty so add a target
            if self.camera_target:
                self.constraint = pm.pointConstraint(self.camera_target, self.tracker_grp)
#            self.set_view(self.tracker_cam[0])
        print "init completed"



    def retarget(self, *args):

        if self.camera_target:
            pm.delete(self.constraint)
            self.constraint = pm.pointConstraint(self.camera_target, self.tracker_grp)
            return 'swapping target to <hl>%s</hl>\n' % self.camera_target
        else:
            return "<span style=\"color:#F05A5A;\">Error:</span> no selection to update tracker.\n"

    def set_view(self, __camera):

        pm.xform(__camera, worldSpace=True, absolute=True, translation=self.current_t)
        pm.xform(__camera, absolute=True, rotation=self.current_r)

    def swap_view(self, *args):
        state = {"tracker": True, "persp": False}
        _state = state[args[0]]
        panel = pm.getPanel(withFocus=True)
        pm.lookThru(self._cameras[_state], panel)
        self.set_view(self._cameras[_state])

        return 'looking through <hl>%s</hl>' % self._cameras[_state][0]


def check_nodes():
    # agg horrible
    cam_list = pm.ls(cameras=True)
    camera_target = pm.ls(selection=True)
    # any camera called tracker?
    _tracker = pm.listTransforms(fnmatch.filter(cam_list, '*tracker*'))
    if not _tracker:
        # no tracking camera found
        tracker_cam = pm.camera(name='tracker_cam')
        tracker_grp = pm.group(empty=True, world=True, name="tracker_grp")
        pm.parent(tracker_cam[0], tracker_grp)
        constraint = pm.listRelatives(tracker_grp, type='pointConstraint')

        print "camera target", camera_target
        if camera_target:
            if not constraint:
                # constraint list is empty so add a target
                if camera_target:
                    constraint = pm.pointConstraint(camera_target, tracker_grp)
    print "checking nodes complete"
    pm.select(camera_target, replace=True)