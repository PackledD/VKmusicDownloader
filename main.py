import sys
sys.path.insert(0, "./libs")
sys.path.insert(1, "./libs/gui")
import login
from log import Logging
from PyQt5.QtWidgets import *
from logging import getLogger
getLogger().setLevel('ERROR')

try:
    app = QApplication(sys.argv)
    ui = login.Log_root()
    ui.show()
    sys.exit(app.exec_())
except KeyboardInterrupt:
    Logging("Stop programm by yourself", user.logfile)
    raise SystemExit
except Exception as err:
    Logging('[ERROR]' + str(err), user.logfile)
    raise SystemExit
