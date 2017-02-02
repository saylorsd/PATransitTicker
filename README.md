# PATransitTicker
Display upcoming Port Authority of Allegheny County bus/T times on a scrolling LED message board connected to a Raspberry Pi.


## Required Parts
1. RaspberryPi (pretty sure any version will work)
2. MAX7219 controlled LED matrix(ces) I happend to use [this one](https://www.amazon.com/gp/product/B01EJ1AFW8/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) but any MAX7219-controlled LED Matrix(ces) should work (with a little coding).


## Accessing TrueTime API
Make an account [here](http://realtime.portauthority.org/bustime/createAccount.jsp) to request an API key.  
An account is also necessary to access the TrueTime documentation.


## Installation
0. Connect Matrix to Raspberry Pi (see my [LED Ticker's readme](https://github.com/saylorsd/led-matrix-ticker) for an example)
1. Clone this repo onto your Raspberry Pi and generate a settings file.  
  ```
  git clone --recursive https://github.com/saylorsd/PATransitTicker
 
  cd PATransitTicker
 
  cp settings-example.py settings.py
  ```
2. Open `settings.py` in your favorite text editor and copy your API key in place of "YOUR_API_KEY_HERE!"  
  ```
  nano settings.py
  ```
3. Adjust the other settings if necessary.
4. Install the necessary python libraries  
  ``` 
  pip install -r requirements.txt  
  ```
5. Run the ticker
  ```
  python ticker.py
  ```
  
  
## Settings
`settings.py`
```python
API_KEY = "YOUR_API_KEY_HERE!"              # TrueTime API key from Port Authority

FONT = CP437_FONT_ROTATED                   # !! Change this to your font of choice (be sure to import it above!)
LOG_FILE = "/home/pi/logs/bus-ticker.log"   # Where the log file will go.  Use Falsey value to log to stdout
DURATION = 30                               # Number of minutes you want it to run for
SPEED = 5
PREDICTIONS = [
    {
        'stpid': 8161,      # stop id
        'rt': 'P3',         # bus route name
        'dir': 'INBOUND'    # direction: 'INBOUND' or 'OUTBOUND'
    },
    {
        'stpid': 18141,
        'rt': '75',
        'dir': 'INBOUND'
    }
]
```


## The Predictions Request
This code uses the `getpredictions` endpoint for the TrueTime API.  For this use case, it sends a bus stop ID, a route ID, and the direction (inbound/outbound).  

You can find your bus stops' IDs on the [Port Authority's Transit Stop Data on the Western Pennsylvania Regional Data Center](https://data.wprdc.org/dataset/port-authority-of-allegheny-county-transit-stops). Find your stop on the map, click it, and look for 'ID' in the popup.

More info can be found in [the documentation](http://realtime.portauthority.org/bustime/apidoc/v1/main.jsp?section=predictions.jsp). (requires you to be logged into the TrueTime site first)


## Cron Job
I built this around my use case wherein I run this script as a cron job that starts around the time I'm getting ready in the morning. For those unfamliar with cron, [here's a nice resource](http://www.adminschoice.com/crontab-quick-reference).  

To edit your cron jobs:  
`crontab -e`  
Then add a line like this:  
`0 7 * * * python /path/to/ticker.py`  


## Extra Resources
* [Port Authority's Developer Resources](http://www.portauthority.org/paac/CompanyInfoProjects/DeveloperResources.aspx)  
* [My LED Matrix Ticker Code](https://github.com/saylorsd/led-matrix-ticker)  
* [TrueTime Documentation](http://realtime.portauthority.org/bustime/apidoc/v1/main.jsp?section=documentation.jsp) (must be logged into * [TrueTime account](http://realtime.portauthority.org/bustime/updateDeveloper.jsp))
