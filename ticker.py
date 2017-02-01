#!/usr/bin/env python
import sys
import requests
import xml.etree.ElementTree as ET
from datetime import datetime as dt, timedelta

from led_matrix_ticker.led import LEDMatrixTicker as Ticker  # TODO: come up with better naming and organization

from settings import API_KEY, LOG_FILE, DURATION, FONT, SPEED

# ==============================================================================
# CONSTANTS
# ==============================================================================
API_URL = 'http://realtime.portauthority.org/bustime/api/v1/getpredictions'

end_time = dt.now() + timedelta(minutes=DURATION)
SPEED = (SPEED % 10) + 1

# Fun Characters
SMILE =     chr(0x01)
HEART =     chr(0x03)
DIAMOND =   chr(0x04)
CLUB =      chr(0x05)
SPADE =     chr(0x06)

MALE = chr(0x0B)
FEMALE = chr(0x0C)

EIGTH_NOTE = chr(0x0D)
DOUBLE_EIGTH_NOTE = chr(0x0E)



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


# ==============================================================================
# STOPS AND ROUTES
# list of dicts that represent each prediction I'd like to see results on
# the keys match the parameters on teh API
# ==============================================================================
p_requests = [
    {
        'stpid': 8161,  # stop id -- see readme for more details
        'rt': 'P3',  # bus route name
        'dir': 'INBOUND'  # direction: 'INBOUND' or 'OUTBOUND'
    },
    {
        'stpid': 18141,
        'rt': '75',
        'dir': 'INBOUND'
    }
]

# ==============================================================================
# LED MATRIX SCROLLING TEXT TICKER
# * in dictionary form for easy reading
# ==============================================================================
ticker = Ticker(width=4, brightness=3, font=FONT, rotated=True)  # settings for my 1x4 matrix display
scroll_times = 20  # number of times to scroll message before checking for new times

# ==============================================================================
# SEND REQUESTS TO PORT AUTHORITY'S REALTIME API
# ==============================================================================
# for each stop, route, direction combination provide above, find the
# next arrival time and print it on the ticker `scroll_times` times
# stop once it's past `end_time`
# ==============================================================================

try:
    while (dt.now() < end_time):
        message = ""
        for request in p_requests:
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
                        message += "{}: {} ({:.0f}mins) |".format(request['rt'], arrival.strftime('%H:%M'),
                                                                  (time.seconds / 60))

                else:  # no predictions often means that a bus isn't coming in the next 30 minutes
                    log('[ERROR] - no predictions for {}'.format(request['rt']))  #

            else:
                log('ERROR] - request error (code: {})'.format(response.status_code))
                message = "API ERROR"

        if not message:
            message = "0 Buses Predicted Within Next 30 Minutes " + HEART

        message = message.replace('|', DOUBLE_EIGTH_NOTE)
        ticker.scroll_message(message, speed=SPEED, repeats=scroll_times)

    log('It ran without error!!')

finally:
    ticker.clear_all()
