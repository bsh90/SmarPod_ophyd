from smarpod_test import SmarPod

from ophyd import Device, Signal
from ophyd import Component as Cpt


class SmarPod_ophyd(Device):
    positions = Cpt(Signal)

    def set_and_get_positions(self, initial_position):
        smarpod_object = SmarPod()
        handle = smarpod_object.set_up()

        final_pose = smarpod_object.moving(handle, initial_position)
        self.positions.set(smarpod_object.pose_to_str(final_pose)).wait()

        smarpod_object.tear_down(handle)

        return self.positions.get()
