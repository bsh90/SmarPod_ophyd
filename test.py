import smaract.smarpod
import logging
import time

model = 10052
locator = "usb:sn:MCS2-00006657"
logging.basicConfig(filename='smarpodAPI.log', filemode='w', 
                    format='%(name)s - %(levelname)s - %(message)s')


class SmarPod_functions():

    def __init__(self, model, locator):
        self.model = model
        self.locator = locator

    def check_lib_compatibility(self):
        # Check Python API major version number vs loaded shared library. 
        v_api = smarpod.api_version
        v_lib = smarpod.GetDLLVerrsion()
        if vapi[0] != vlib[0]:
            logging.error("incompatible python api: %s and library version: %s" % (v_api, v_lib))
            raise RuntimeError("incompatible python api and library version")

    def set_up(self, model, locator):
        try:
            self.log_controllers()

            smarpod_handle = smarpod.Open(model, locator)
            logging.info("Device opened successfully")

            frequency = 8000
            smarpod.Set_ui(smarpod_handle, smarpod.Property.FREF_AND_CAL_FREQUENCY, frequency)
            logging.info("Frequency for referencing and calibration is set to %d", frequency)

            smarpod.Calibrate(handle)
            logging.info("Device has been calibrated.")

            if not smarpod.IsReferenced(smarpod_handle):
                smarpod.Set_ui(h, smarpod.Property.FREF_METHOD, smarpod.DEFAULT)
                smarpod.FindReferenceMarks(handle)
                logging.info("Referencing was successful")

            smarpod.SetSensorMode(handle, smarpod.SensorPowerMode.ENABLED)

            move_status = smarpod.GetMoveStatus(smarpod_handle)
            while (move_status == SMARPOD_CALIBRATING or move_status == SMARPOD_REFERENCING):
                logging.warning("movement status = %s (%s). Operation will wait for 3 second." % (smarpod.MoveStatus(mstat), move_status))
                time.sleep(3)
            smarpod.Stop(smarpod_handle)
            move_status = smarpod.GetMoveStatus(smarpod_handle)
            if (move_status != SMARPOD_STOPPED):
                logging.info("Moving stopped. movement status = %s (%s)" % (smarpod.MoveStatus(move_status), move_status))
            else:
                logging.error("Moving stopped. movement status = %s (%s). It could not be stopped." % (smarpod.MoveStatus(move_status), move_status))
                raise smarpod.Error



            return smarpod_handle
        except smarpod.Error as err:
            error_message = "SMARPOD ERROR: %s -> %s - (%s)" % (err.func, smarpod.ErrorCode(err.code), err.code)
            logging.error(error_message)
            print(error_message)
            smarpod.Close(smarpod_handle)

    def tear_down(self, handle):
        if smarpod_handle != None:
            smarpod.Close(smarpod_handle)
            logging.info("Device closed successfully")
            smarpod_handle = None

    def log_controllers(self):
        sysList = smarpod.FindSystems().splitlines()
        for sys in sysList:
            logging.info("controllers found: %s \n" % sys)






smarpod_object = SmarPod_functions(model, locator)
handle = smarpod_object.set_up(smarpod_handle)
smarpod_object.tear_down(self, handle)