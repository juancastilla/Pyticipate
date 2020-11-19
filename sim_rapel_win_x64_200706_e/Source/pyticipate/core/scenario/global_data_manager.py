import importlib
import os
from threading import Semaphore
import uuid

class GlobalDataManager():

    def __init__(self):
        self._lock = Semaphore(value=1)

        self._global_datas = {}

        filepath = os.environ.get('GLOBAL_DATA_PY')
        if filepath is None:
            raise ValueError('No Global Data Manager found!')
        filename = os.path.split(filepath)[1]
        self._module = self._load_plugin_module(filename, filepath)

    def _load_plugin_module(self, name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def _create_new_global_data_instance(self, id):
        return self._module.GlobalData()

    def get_global_data(self, session):
        self._lock.acquire()
        if 'id' not in session:
            id = uuid.uuid4()
            session['id'] = id
            self._global_datas[id] = self._create_new_global_data_instance(id)
        else:
            id = session['id']
            if id not in self._global_datas:
                self._global_datas[id] = self._create_new_global_data_instance(id)
        self._lock.release()
        return self._global_datas[id]
