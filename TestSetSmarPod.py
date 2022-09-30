from smaract.smarpod import Pose as Pose
import smaract.smarpod as smarpod
from smarpod_main import SmarPod
import unittest
import time


class TestSmarPod(unittest.TestCase):

    def set(self, pose, handle, smarpod_object):
        self.verify_reachable_position(pose, handle)

        print("moving to %s" % smarpod_object.pose_to_str(pose))
        smarpod.Move(handle, pose, 0, True)

        time.sleep(1)
        self.verify_stopped_status(handle)
        return self.get_status(handle)

    def get_status(self, handle):
        move_status = smarpod.GetMoveStatus(handle)
        if (move_status == smarpod.MoveStatus.STOPPED):
            return True
        else:
            return False

    def verify_stopped_status(self, handle):
        if not self.get_status(handle):
            error = Exception("Status can not be stopped.")
            raise error

    def check_pose(self, pose, handle):
        if not smarpod.IsPoseReachable(handle, pose):
            return False
        else:
            return True

    def verify_reachable_position(self, pose, handle):
        if not self.check_pose(pose, handle):
            raise Exception("Not all poses in sequence are reachable")


    def load_position_data_sample(self):
        pose_Home = Pose(0, 0, 0, 0, 0, 0)
        pose_sequence = [
            pose_Home,
            Pose(0, 0, -0.001, 0, 0, 5),
            Pose(0, 0, -0.001, 0, 0, 7),
            Pose(0, 0, -0.001, 0, 0, 9),
            Pose(0, 0, -0.001, 0, 0, 11),
            Pose(0, 0, -0.001, 0, 0, 13),
            Pose(0, 0, -0.001, 0, 0, 14),
        ]
        return pose_sequence

    def test_set_pos(self):
        pose_seq = self.load_position_data_sample()
        smarpod_object = SmarPod()
        handle = smarpod_object.set_up()

        for pose in pose_seq: 
            status = self.set(pose, handle, smarpod_object)
            newPose = smarpod.GetPose(handle)
            print(smarpod_object.pose_to_double_list(newPose))

        smarpod_object.tear_down(handle)


if __name__ == "__main__":
    unittest.main()
