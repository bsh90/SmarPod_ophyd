import sys
sys.path.append('/.../src')

from smaract.smarpod import Pose as Pose
from SmarPodMain import SmarPod
from OphydSmarPod import SmarSignalRO, SmarSignal
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
        hexapod = SmarSignalRO(name="hexapod")
        for i in range(10):
            print(hexapod.get())
        hexapod.tear_down()

    def test_happy_path_set_position(self):
        pose_seq = self.load_position_data_sample()

        hexapod = SmarSignal(name="hexapod")
        for pose in pose_seq: 
            status = hexapod.set(pose)
            print("done={0.done}, success={0.success}".format(status))
        hexapod.tear_down()

    def test_happy_path_get_and_set_with_same_handle(self):
        hexapod_get = SmarSignalRO(name="hexapod_get")
        print("Initial position is ", hexapod_get.get())

        hexapod_set = SmarSignal(name="hexapod_set", 
                                 optional_handle=hexapod_get.handle)
        pose_seq = self.load_position_data_sample()
        for pose in pose_seq: 
            status = hexapod_set.set(pose)
            print("done={0.done}, success={0.success}".format(status))

        print("Last position is ", hexapod_set.get(), hexapod_get.get())

        hexapod_set.tear_down()


if __name__ == "__main__":
    unittest.main()
