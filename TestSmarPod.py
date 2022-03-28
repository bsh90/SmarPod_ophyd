from smaract.smarpod import Pose as Pose
from smarpod_test import SmarPod
from ophyd_test import SmarSignalRO, SmarSignal
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

#     def test_happyPath(self):
#         pose_seq = self.load_position_data_sample()

#         smarpod_object = SmarPod()
#         handle = smarpod_object.set_up()

#         get_pose = smarpod_object.moving(handle, pose_seq)
#         final_pose_zero = smarpod_object.pose_to_str(get_pose)

#         smarpod_object.tear_down(handle)

# #        self.assertEqual(final_pose_zero, initial_pose_zero)
#         print(final_pose_zero)

    def test_happy_path_get_position(self):
        with SmarSignalRO(name="sth1") as ophyd_object:
            pose = ophyd_object.get()
        print(pose)

    def test_happy_path_set_position(self):
        pose_seq = self.load_position_data_sample()

        for pose in pose_seq:
            with SmarSignal(name="sth1") as ophyd_object:
                status = ophyd_object.set(pose)
            print("done={0.done}, success={0.success}".format(status))


if __name__ == "__main__":
    unittest.main()
