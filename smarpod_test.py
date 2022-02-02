import smaract.smarpod as smarpod
from smaract.smarpod import Pose as Pose
import logging
import asyncio


class SmarPod:

    model = 10052
    locator = "usb:sn:MCS2-00006657"
    logging.basicConfig(
        filename="smarpodAPI.log",
        filemode="w",
        format="%(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )

    def __init__(self, pose_sequence):
        self.handle = None
        self.pose_sequence = pose_sequence

    def check_lib_compatibility(self):
        # Check Python API major version number vs loaded shared library.
        v_api = smarpod.api_version
        v_lib = smarpod.GetDLLVersion()
        if v_api[0] != v_lib[0]:
            logging.error(
                "incompatible python api: %s and library version: %s" % (v_api, v_lib)
            )
            raise RuntimeError("incompatible python api and library version")

    def log_controllers(self):
        sysList = smarpod.FindSystems().splitlines()
        for sys in sysList:
            logging.info("controllers found: %s \n" % sys)

    def pose_to_str(self, pose):
        return "%s,%s,%s,%s,%s,%s" % (
            pose.positionX,
            pose.positionY,
            pose.positionZ,
            pose.rotationX,
            pose.rotationY,
            pose.rotationZ,
        )

    def set_speed_and_frequency_and_pivot_point_and_coordinate_system(self):
        smarpod.SetSpeed(self.handle, 1, 3e-3)
        smarpod.SetMaxFrequency(self.handle, 18500)

        smarpod.Set_ui(
            self.handle, smarpod.Property.PIVOT_MODE, smarpod.PivotMode.RELATIVE
        )
        smarpod.SetPivot(self.handle, [10e-3, 0, 0])

        coordinate_sys = Pose(0.0, 0.0, 0.0, 1.5, 0.0, 0.0)
        smarpod.SetCoordinateSystem(self.handle, coordinate_sys)
        logging.info(
            "setting coordinate system to %s" % self.pose_to_str(coordinate_sys)
        )

    async def set_up(self):
        try:
            self.check_lib_compatibility()
            self.log_controllers()

            self.handle = smarpod.Open(model, locator)
            logging.info("Device opened successfully")

            frequency = 8000
            smarpod.Set_ui(
                self.handle, smarpod.Property.FREF_AND_CAL_FREQUENCY, frequency
            )
            logging.info(
                "Frequency for referencing and calibration is set to %d", frequency
            )

            smarpod.Calibrate(self.handle)
            logging.info("Device has been calibrated.")

            if not smarpod.IsReferenced(self.handle):
                smarpod.Set_ui(
                    self.handle, smarpod.Property.FREF_METHOD, smarpod.DEFAULT
                )
                smarpod.FindReferenceMarks(self.handle)
                logging.info("Referencing was successful")

            smarpod.SetSensorMode(self.handle, smarpod.SensorPowerMode.ENABLED)

            move_status = smarpod.GetMoveStatus(self.handle)
            while (
                move_status == smarpod.MoveStatus.CALIBRATING
                or move_status == smarpod.MoveStatus.REFERENCING
            ):
                logging.warning(
                    "movement status = %s (%s). Operation will wait for 3 second."
                    % (smarpod.MoveStatus(mstat), move_status)
                )
                await asyncio.sleep(3)
            smarpod.Stop(self.handle)
            move_status = smarpod.GetMoveStatus(self.handle)
            if move_status == smarpod.MoveStatus.STOPPED:
                logging.info(
                    "Moving stopped. movement status = %s (%s)"
                    % (smarpod.MoveStatus(move_status), move_status)
                )
            else:
                logging.error(
                    "Moving stopped. movement status = %s (%s). It could not be stopped."
                    % (smarpod.MoveStatus(move_status), move_status)
                )
                raise Exception("It could not be stopped.")

            self.set_speed_and_frequency_and_pivot_point_and_coordinate_system()

        except (smarpod.Error, Exception) as err:
            error_message = "SMARPOD ERROR: %s -> %s - (%s)" % (
                err.func,
                smarpod.ErrorCode(err.code),
                err.code,
            )
            logging.error(error_message)
            print(error_message)

    def tear_down(self, smarpod_handle):
        if smarpod_handle != None:
            smarpod.Close(smarpod_handle)
            logging.info("Device closed successfully")
            smarpod_handle = None

    def check_pose_list(self, pose_list):
        for pose in pose_list:
            if not smarpod.IsPoseReachable(self.handle, pose):
                return False
        return True

    def move_sequence(self, seq):
        for pose in seq:
            print("moving to %s" % self.pose_to_str(pose))
            smarpod.Move(self.handle, pose, 0, True)

    def moving(self):
        if not self.check_pose_list(self.pose_sequence):
            raise Exception("not all poses in sequence are reachable")
        self.move_sequence(self.pose_sequence)

        pose = smarpod.GetPose(self.handle)
        logging.info("pose = %s" % self.pose_to_str(pose))
        return pose
