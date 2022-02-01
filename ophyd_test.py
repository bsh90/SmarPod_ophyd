import test as smarPodHandler

from ophyd.utils import make_dir_tree
import datetime
from databroker import Broker, temp
from bluesky.run_engine import RunEngine

from ophyd import Device, Signal
from ophyd import Component as Cpt
from ophyd.sim import NullStatus, new_uid
import numpy as np
from pathlib import Path
import time




class SmarPodFileHandler:
    spec = {'smarpod'}

    def __init__(self, filename):
        self._name = filename

    def __call__(self):
        return np.load(self._name)


_ = make_dir_tree(datetime.datetime.now().year, base_path='/tmp/data')
db = Broker.from_config(temp())
db.reg.register_handler('smarpod', SmarPodFileHandler, overwrite=True)

RE = RunEngine({})
token = RE.subscribe(db.insert)


class SmarPod(Device):
    movement = Cpt(Signal)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.numpy_file = None
        self.resource_id = None
        

    def trigger(self):
        super().trigger()

        datum_id = new_uid()
        date = datetime.datetime.now()
        self.numpy_file = Path('/tmp/data') / Path(date.strftime('%Y/%m/%d')) / \
                          Path('{}.npy'.format(datum_id))
        time.sleep(1)
        self.movement.put(datum_id)

        self.resource_id = db.reg.insert_resource('smarpod', self.numpy_file, {})
        db.reg.insert_datum(self.resource_id, datum_id, {})
        time.sleep(1)

        return NullStatus()

