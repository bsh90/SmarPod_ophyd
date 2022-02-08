from smarpod_test import SmarPod

from ophyd import Device, Signal
from ophyd import Component as Cpt
import asyncio


class SmarPod_ophyd(Device):
    positions = Cpt(Signal)

    def set_and_get_positions(self, initial_position):
        smarpod_object = SmarPod()
        handle = smarpod_object.set_up()

        self.positions.set(smarpod_object.moving(initial_position)).wait()

        smarpod_object.tear_down(handle)

        return print(self.positions.get())
