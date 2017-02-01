#==============================================================================
# SETTINGS
#==============================================================================
from led_matrix_ticker.fonts import CP437_FONT_ROTATED          # !! ADD YOUR FONT CHOICE HERE

API_KEY = "YOUR_API_KEY_HERE!"

FONT = CP437_FONT_ROTATED                   # !! Change this to your font of choice (be sure to import it above!)
LOG_FILE = "/home/pi/logs/bus-ticker.log"   # Where the log file will go.  Use Falsey value to log to stdout
DURATION = 30                               # Number of minutes you want it to run for