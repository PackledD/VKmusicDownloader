import sys
sys.path.insert(0, "./libs")
import auth
import music
from log import Logging


try:
    user = auth.auth('', '')
    user.session_start()
    music.get_songs_info(user)
    # music.download_song('Gloryhammer - Apocalypse 1992', user)
except KeyboardInterrupt:
    Logging("Stop programm by yourself", user.logfile)
    raise SystemExit
except Exception as err:
    Logging('[ERROR]' + str(err), user.logfile)
    raise SystemExit
