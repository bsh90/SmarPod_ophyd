from ophyd import Signal, StatusBase
import smaract.smarpod as smarpod
from smarpod_test import SmarPod
import logging


class SmarSignalRO(Signal):
    smarpod_object = None
    handle = None

    def __enter__(self):
        self.smarpod_object = SmarPod()
        self.handle = self.smarpod_object.set_up()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.smarpod_object.tear_down(self.handle)

    def get(self):
        pose = smarpod.GetPose(self.handle)
        return self.smarpod_object.pose_to_double_list(pose)


class SmarSignal(SmarSignalRO):
    status = None

    def __enter__(self):
        super().__enter__()
        self.status = StatusBase(timeout=60)
        return self

    def set(self, pose):
        self.verify_reachable_position(pose)

        print("moving to %s" % self.smarpod_object.pose_to_str(pose))
        smarpod.Move(self.handle, pose, 0, True)

        self.verify_stopped_status()
        return self.status

    def get_status(self):
        move_status = smarpod.GetMoveStatus(self.handle)
        if (move_status == smarpod.MoveStatus.STOPPED):
            self.status.set_finished()
            self.status.wait(5)
            return True
        else:
            return False

    def verify_stopped_status(self):
        if not self.get_status():
            error = Exception("Status can not be stopped.")
            self.status.set_exception(error)
            raise error

    def check_pose(self, pose):
        if not smarpod.IsPoseReachable(self.handle, pose):
            return False
        else:
            return True

    def verify_reachable_position(self, pose):
        if not self.check_pose(pose):
            raise Exception("Not all poses in sequence are reachable")