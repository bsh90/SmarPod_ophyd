from ophyd import Signal, StatusBase
import smaract.smarpod as smarpod
from SmarPodMain import SmarPod
from collections import OrderedDict
import time
import datetime
import logging


class SmarSignalRO(Signal):
    smarpod_object = None
    handle = None

    def __init__(self, name, optional_handle=None):
        super().__init__(name=name)
        self.smarpod_object = SmarPod()
        if optional_handle is not None:
            self.handle = optional_handle
        else:
            self.handle = self.smarpod_object.set_up()

    def tear_down(self):
        self.smarpod_object.tear_down(self.handle)

    def get(self):
        pose = smarpod.GetPose(self.handle)
        return self.smarpod_object.pose_to_double_list(pose)

    def read(self):
        secondary_orderedDict = OrderedDict()
        secondary_orderedDict['value'] = self.get()
        time_now = datetime.datetime.now()
        secondary_orderedDict['timestamp'] = datetime.datetime.timestamp(time_now)
        
        main_orderedDict = OrderedDict()
        main_orderedDic['channel1'] =  secondary_orderedDict
        return main_orderedDic

    def describe(self):
        secondary_orderedDict = OrderedDict()
        secondary_orderedDict['source'] = 'source'
        secondary_orderedDict['dtype'] = 'number'
        secondary_orderedDict['shape'] = []
        
        main_orderedDict = OrderedDict()
        main_orderedDic['channel1'] =  secondary_orderedDict
        return main_orderedDic

    def read_configuration(self):
        return OrderedDict()

    def describe_configuration(self):
        return self.read_configuration()

    def trigger(self):
        move_status = smarpod.GetMoveStatus(self.handle)
        status = StatusBase(timeout=60)
        while (move_status is not smarpod.MoveStatus.STOPPED):
            time.sleep(10)
        status.set_finished()
        status.wait(5)
        return status


class SmarSignal(SmarSignalRO):
    status = None

    def set(self, pose):
        self.verify_reachable_position(pose)

        print("moving to %s" % self.smarpod_object.pose_to_str(pose))
        smarpod.Move(self.handle, pose, 0, True)

        self.status = StatusBase(timeout=60)
        self.verify_stopped_status()
        status_result = self.status
        self.status = None

        return status_result

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


class SmarSignalDifferentAxis(SmarSignalRO):
    def set(self, i, i_value):
        hexapod_get = SmarSignalRO(name="hexapod_get")
        pose = hexapod_get.get()
        pose[i] = i_value 
        hexapod_set = SmarSignal(name="hexapod_set", 
                                 optional_handle=hexapod_get.handle)
        return hexapod_set.set(pose)


class SmarSignalXPosition(SmarSignalDifferentAxis):
    def set(self, x, x_value):
        super().set(0, x_value)


class SmarSignalYPosition(SmarSignalDifferentAxis):
    def set(self, y, y_value):
        super().set(1, y_value)


class SmarSignalZPosition(SmarSignalDifferentAxis):
    def set(self, z, z_value):
        super().set(2, z_value)


class SmarSignalXRotation(SmarSignalDifferentAxis):
    def set(self, x, x_value):
        super().set(3, x_value)


class SmarSignalYRotation(SmarSignalDifferentAxis):
    def set(self, y, y_value):
        super().set(4, y_value)


class SmarSignalZRotation(SmarSignalDifferentAxis):
    def set(self, z, z_value):
        super().set(5, z_value)