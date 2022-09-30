from smaract.smarpod import Pose as Pose
import smaract.smarpod as smarpod
from smarpod_main import SmarPod
import unittest


class TestSmarPod(unittest.TestCase):

    def test_happy_path_get_position(self):
        smarpod_object = SmarPod()
        handle = smarpod_object.set_up()

        for i in range(10):
            pose = smarpod.GetPose(handle)
            print(smarpod_object.pose_to_double_list(pose))

        smarpod_object.tear_down(handle)

if __name__ == "__main__":
    unittest.main()
