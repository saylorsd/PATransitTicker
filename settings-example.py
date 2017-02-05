#==============================================================================
# SETTINGS
#==============================================================================
from led_matrix_ticker.fonts import CP437_FONT_ROTATED          # !! ADD YOUR FONT CHOICE HERE

API_KEY = "YOUR_API_KEY_HERE!"              # TrueTime API key from Port Authority

LOG_FILE = "/home/pi/logs/bus-ticker.log"   # Where the log file will go.  Use Falsey value to log to stdout

USE_REDIS = False                           # Set to true if publishing message to redis to be consumed by another ticker

# TICKER SETTINGS
# only used if USE_REDIS is False
FONT = CP437_FONT_ROTATED                   # !! Change this to your font of choice (be sure to import it above!)
DURATION = 30                               # Number of minutes you want it to run for
WIDTH = 4                                   # Width of ticker (i.e. number of matrices)
BRIGHTNESS = 1                              # LED brightness: 0-15
SPEED = 5                                   # Message speed 1-10
SCROLL_TIMES = 10                           # number of times to scroll message before checking for new times

# REDIS SETTINGS
# only used if USE_REDIS is True
REDIS_DB = 0                                # probably don't need to change this
REDIS_HOST = 'localhost'                    # probably don't need to change this
REDIS_PORT = '6379'                         # probably don't need to change this

REDIS_MSG_KEY = 'ticker_msg'                # the redis key to which you'll write the message


# ==============================================================================
# STOPS AND ROUTES
# list of dicts that represent each prediction I'd like to see results on
# the keys match the parameters on the API
# ==============================================================================
PREDICTIONS = [
    {
        'stpid': 8161,      # stop id -- see readme for more details
        'rt': 'P3',         # bus route name
        'dir': 'INBOUND'    # direction: 'INBOUND' or 'OUTBOUND'
    },
    {
        'stpid': 18141,
        'rt': '75',
        'dir': 'INBOUND'
    }
]