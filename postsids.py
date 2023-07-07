import requests
from datetime import datetime
import time
import sys

args = list(sys.argv)[1:]

source = 0
noradID = 0
lat = 0
long = 0

def init(s,nid,la,lo):
    global source
    global noradID
    global lat
    global long

    source = str(s)
    noradID = int(nid)
    lat = float(la)
    long = float(lo)

    return 0
    

def send_sids(bcn):
    DB_TELEMETRY_ENDPOINT_URL= "https://db.satnogs.org/api/telemetry/"
    # SiDS parameters
    params = {
        'noradID': noradID,
        'source': str(source), 
        'timestamp': datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S.000Z'), 
        'locator': 'longLat', 
        'longitude': long, 
        'latitude': lat, 
        'frame': str(bcn), 
    }
    #print(DB_TELEMETRY_ENDPOINT_URL, params)
    postSuccess = False
    while(not postSuccess):
        try:
            response = requests.post(DB_TELEMETRY_ENDPOINT_URL, data=params, timeout=10)
            print(response)
            response.raise_for_status()
            postSuccess = True
            print("Posted frame to Satnogs!")
        except Exception as e:
            
            print('Could not post data to Satnogs, retrying.', e)
            time.sleep(0.5)
    return

