from smaract.smarpod import Pose as Pose
from smarpod_test import SmarPod
from ophyd_test import SmarSignalRO, SmarSignal
import unittest


class TestSmarPod(unittest.TestCase):

    def test_happy_path_get_position(self):
        hexapod = SmarSignalRO(name="hexapod")
        for i in range(10):
            print(hexapod.get())
        hexapod.tear_down()

if __name__ == "__main__":
    unittest.main()
