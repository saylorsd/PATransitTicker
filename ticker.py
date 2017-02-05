#!/usr/bin/env python
import time
import xml.etree.ElementTree as ET
import requests
import redis

from datetime import datetime as dt, timedelta

from led_matrix_ticker import LEDMatrixTicker as Ticker  # TODO: come up with better naming and organization

from settings import API_KEY, LOG_FILE, USE_REDIS, \
    DURATION, FONT, SPEED, PREDICTIONS, SCROLL_TIMES, BRIGHTNESS, WIDTH, \
    REDIS_DB, REDIS_HOST,  REDIS_MSG_KEY, REDIS_PORT

# ==============================================================================
# CONSTANTS
# ==============================================================================
API_URL = 'http://realtime.portauthority.org/bustime/api/v1/getpredictions'

end_time = dt.now() + timedelta(minutes=DURATION)
SPEED = (SPEED % 10) + 1

# Fun Characters
SMILE = chr(0x01)
_SMILE = chr(0x02)
HEART = chr(0x03)
DIAMOND = chr(0x04)
CLUB = chr(0x05)
SPADE = chr(0x06)

MALE = chr(0x0B)
FEMALE = chr(0x0C)

EIGTH_NOTE = chr(0x0D)
DOUBLE_EIGTH_NOTE = chr(0x0E)

SPLIT = DIAMOND

if USE_REDIS:
    redis_conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
else:
    # instantiate LED Matrix Ticker controller
    ticker = Ticker(width=WIDTH, brightness=BRIGHTNESS, font=FONT, rotated=True)  # settings for my 1x4 matrix display



def log(msg, file=LOG_FILE, mode='w', display=True):
    """
    Writes `msg` to log file at path `log_file`

    :param msg: str: message to write in log
    :param file: str: path/to/log.txt
    :param mode: file open mode
    """
    if file:
        with open(file, mode) as f:
            f.write("{}  ::  {}\n".format(dt.now().isoformat(), msg))
    elif display:
        print(msg)


def get_message():
    """
    For each stop, route, direction combination provide above, find the
    next arrival time make a nice string out of the information
    :return: message to send to ticker
    """

    message = ""
    for request in PREDICTIONS:
        request.update({'key': API_KEY})  # add my api key to request parameters
        response = requests.get(API_URL, params=request)  # make request to API
        # see readme for example result
        if response.status_code == 200:
            results = ET.fromstring(response.text)  # parse the XML response into an ElementTree
            log(request['rt'])

            if not results.findall('error'):
                prediction = results.findall('prd')[0]  # per API: first prediction result == next arrival

                if len(prediction):
                    arrival = dt.strptime(prediction.findall('prdtm')[0].text, "%Y%m%d %H:%M")
                    time = arrival - dt.now()
                    message += "{}: {} ({:.0f}mins) | ".format(request['rt'], arrival.strftime('%H:%M'),
                                                               (time.seconds / 60))

            else:  # no predictions often means that a bus isn't coming in the next 30 minutes
                log('[ERROR] - no predictions for {}'.format(request['rt']))

        else:
            log('ERROR] - request error (code: {})'.format(response.status_code))
            message = "API ERROR"

    if not message:
        message = "0 Buses Predicted Within Next 30 Minutes " + SPLIT

    message = message.replace('|', SPLIT)

    return message

# MAIN LOOP
try:
    while (dt.now() < end_time):
        message = get_message()
        if USE_REDIS:
            test = redis_conn.set(REDIS_MSG_KEY, message)
            time.sleep(60)
        else:
            ticker.scroll_message(message, speed=SPEED, repeats=SCROLL_TIMES)

finally:
    if not USE_REDIS:
        ticker.clear_all()
    else:
        redis_conn.set(REDIS_MSG_KEY, "")
