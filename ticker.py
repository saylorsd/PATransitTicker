import requests
import xml.etree.ElementTree as ET
from datetime import datetime as dt

from led_matrix_ticker.led import LEDMatrixTicker as Ticker     # TODO: come up with better naming and organization
from led_matrix_ticker.fonts import CP437_FONT_ROTATED          # !! ADD YOUR FONT CHOICE HERE

from settings import API_KEY, END_TIME

api_url = 'http://realtime.portauthority.org/bustime/api/v1/getpredictions'
log_file = "bus-ticker.log"  # !! make empty if you don't want to keep a log


end_time = dt.strptime(END_TIME, "%H:%M")
end_time = end_time.replace(year=dt.now().year, month=dt.now().month, day=dt.now().day)

def log(msg, file=log_file, mode='a'):
    """
    Writes `msg` to log file at path `log_file`

    :param msg: str: message to write in log
    :param file: str: path/to/log.txt
    :param mode: file open mode
    """
    if log_file:
        with open(file, mode) as f:
            f.write("{}  ::  {}\n".format(dt.now().isoformat(), msg))


#==============================================================================
# STOPS AND ROUTES
# list of dicts that represent each prediction I'd like to see results on
# the keys match the parameters on teh API
#==============================================================================
p_requests = [
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


#==============================================================================
# LED MATRIX SCROLLING TEXT TICKER
# * in dictionary form for easy reading
#==============================================================================
ticker = Ticker(width=4, brightness=3, font=CP437_FONT_ROTATED,rotated=True)      # settings for my 1x4 matrix display
scroll_times = 20       # number of times to scroll message before checking for new times


#==============================================================================
# SEND REQUESTS TO PORT AUTHORITY'S REALTIME API
#==============================================================================
# for each stop, route, direction combination provide above, find the
# next arrival time and print it on the ticker `scroll_times` times
# stop once it's past `end_time`
#==============================================================================

try:
    message = ""
    while (dt.now() < end_time):
        for request in p_requests:
            request.update({'key': API_KEY})                    # add my api key to request parameters
            response = requests.get(api_url, params=request)    # make request to API
                                                                # see readme for example result
            if response.status_code == 200:
                results = ET.fromstring(response.text)          # parse the XML response into an ElementTree
                print(request['rt'])
                if not results.findall('error'):
                    prediction = results.findall('prd')[0]      # per API: first prediction result == next arrival
                    if len(prediction):
                        arrival = dt.strptime(prediction.findall('prdtm')[0].text, "%Y%m%d %H:%M")
                        time = arrival - dt.now()
                        message += "{}: {} ({:.0f}mins) ||".format(request['rt'], arrival.strftime('%H:%M'), (time.seconds/ 60))

                else:
                    print('[ERROR] - no predictions for {}'.format(request['rt']))
                    log('[ERROR] - no predictions for {}'.format(request['rt']))  # log it

        print(message.rstrip('|'))              # rstrip to remove trailing '||'
        ticker.scroll_message(message, speed=4, repeats=scroll_times)
    log('It ran without error!!')
finally:
    ticker.clear_all()