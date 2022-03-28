from smaract.smarpod import Pose as Pose
from smarpod_test import SmarPod
from ophyd_test import SmarPod_ophyd
import unittest


class TestSmarPod(unittest.TestCase):
    def load_position_data_sample(self):
        pose_Home = Pose(0, 0, 0, 0, 0, 0)
        pose_sequence = [
            pose_Home,
            Pose(0, 0, 0.002, 0, 0, 0),
            Pose(0, 0, -0.002, 0, 0, 0),
            Pose(-0.002, 0, 0, 0, 0, 0),
            Pose(-0.002, -0.002, 0, 0, 0, 0),
            Pose(0.002, 0.002, 0, 0, 0, 0),
            Pose(0, 0, 0, 0, 0, -5),
            Pose(0, 0, 0, -0.02, 0, 5),
            pose_Home,
        ]
        return pose_sequence

    def test_happyPath(self):
        pose_seq = self.load_position_data_sample()

        smarpod_object = SmarPod()
        handle = smarpod_object.set_up()

        get_pose = smarpod_object.moving(handle, pose_seq)
        final_pose_zero = smarpod_object.pose_to_str(get_pose)

        smarpod_object.tear_down(handle)

#        self.assertEqual(final_pose_zero, initial_pose_zero)
        print(final_pose_zero)

    def test_happyPath_ophyd(self):
        pose_seq = self.load_position_data_sample()

        ophyd_object = SmarPod_ophyd("sth", name="sth1")
        final_pose_zero_in_double_list = ophyd_object.set_and_get_positions(pose_seq)

#        self.assertEqual(get_pose, pose_seq)
        print(final_pose_zero_in_double_list)


if __name__ == "__main__":
    unittest.main()
