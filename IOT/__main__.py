#* The main manager
from IOTManager import IOTManager
iot_manager = IOTManager()
iot_manager.run_checks()
iot_manager.start()
del iot_manager