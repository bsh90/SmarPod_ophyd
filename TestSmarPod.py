from smarpod_test import SmarPod
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

        smarpod_object = SmarPod(pose_seq)
        handle = smarpod_object.set_up()

        get_pose = smarpod_object.moving(pose_seq)

        smarpod_object.tear_down(handle)

        self.assertEqual(get_pose, pose_seq)


if __name__ == "__main__":
    unittest.main()
