from smarpod_test import SmarPod

from ophyd import Device, Signal
from ophyd import Component as Cpt
import asyncio


class SmarPod_ophyd(Device):
    movement = Cpt(Signal)

    def __init__(self, *args, position, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_position_data = position
        self.final_position = None

    def set_positions(self):
        smarpod_object = SmarPod(self.initial_position_data)
        handle = smarpod_object.set_up()
        self.final_position = smarpod_object.moving(self.initial_position_data)
        smarpod_object.tear_down(handle)

        return self.final_position
