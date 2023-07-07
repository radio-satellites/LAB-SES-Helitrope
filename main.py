import socket
import time
import sys
from datetime import datetime
import parser
import collections
import time
import geocoder
import earthmath
import postsids as satnogs
from sondehubtools.amateur import Uploader

print("LAB SES 1 MISSION TELEMETRY DECODER/DASHBOARD")
time.sleep(0.5)
print("By VE3SVF")
print("\n")

counter_packet = 0
counter_data = 0
location_works = False




fake_var = 0

#callsign_station = input("Please enter your callsign. If you don't have a callsign, enter N0CALL, followed by a unique ID number, such as N0CALL-576: ")


try:
    g = geocoder.ip('me')
    fake_var = g.latlng
    location_works = True #Otherwise will fail
    print("Location found")
except:
    print("ERROR: CANNOT GET LOCATION")

_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_s.settimeout(1)
num_nochars = 0
try:
    _s.connect(("127.0.0.1",7322))
except:
    print("ERROR: COULD NOT CONNECT TO FLDIGI")
    #exit()


    
f_config = open("config.txt",'r').read().split("\n")[2].split(",")

packet = ""

#init server side stuff
satnogs.init("LABSES",42732,0,0)

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

uploader = Uploader(
    f_config[0], #callsign
    uploader_position=[fake_var[0], fake_var[1], 100], # [latitude, longitude, altitude]
    uploader_radio=f_config[2], # Radio information - Optional
    uploader_antenna=f_config[3] # Antenna information - Optional
)

uploader.upload_station_position(
    f_config[0], #callsign
    [fake_var[0], fake_var[1], 100], # [latitude, longitude, altitude]
    uploader_radio=f_config[2], # Radio information - Optional
    uploader_antenna=f_config[3] # Antenna information - Optional
)


print("Ingest of data has started!")

old_data = ""


try:
    f = open("telemetry_log.txt",'r')
    old_data = f.read()
    f.close()
    
except Exception as e:
    print("Couldn't restore data from an old version",e)

try:
    f = open("telemetry_log.txt",'w')
    f.write(old_data)
except Exception as e:
    print("Couldn't open restore file for writing!",e)

while True:
    try:
         _char = _s.recv(1).decode()
         counter_data = counter_data + 1
         num_nochars = 0
         #print(_char)
         packet = packet + _char #Update buffer
         #print(message)
         if _char == "\n":
             try:
                    
                pressure,altitude,temperature,latitude,longitude,frame_num = parser.parse_string(packet)
                #form server side packet
                server_packet = "00444,"+str(pressure)+","+str(altitude)+","+str(temperature)+","+str(latitude)+","+str(longitude)+","+str(frame_num)
                f.write(server_packet)
                #print(server_packet)
                satnogs.send_sids(server_packet)
                counter_packet = counter_packet+1
                print("=======================NEW FRAME=======================")
                print("----HEADER----")
                print("Frame number: "+str(frame_num))
                print("Frame number of GS: "+str(counter_packet))
                print("--------------")
                print("--------------PAYLOAD--------------")
                print("Pressure: "+str(pressure)+" hPa")
                print("Altitude: "+str(altitude)+" m above sea level")
                print("Temperature (inside): "+str(temperature)+" *C")
                print("-----------------------------------")
                print("------Location Data------")
                print("Latitude: "+str(latitude))
                print("Longitude: "+str(longitude))
                print("Lat/Lng string: "+str(latitude)+","+str(longitude))
                print("-------------------------")
                print("=======================================================")
                print("\n")
                if longitude != 0 and latitude != 0 and altitude != 0:
                    #send to sondehub!
                    print("Send data to sondehub!")
                    uploader.add_telemetry(
                        f_config[1], # Your payload callsign
                        datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), # Time
                        latitude, # Latitude
                        longitude, # Longitude
                        altitude # Altitude
                    )
                if location_works == True and longitude != 0 and latitude != 0 and altitude != 0: #Check all values are correct (more or less)
                    print("=======================SPACECRAFT DATA=======================")
                    print("----GROUND STATION----")
                    print("Frame number of GS: "+str(counter_packet))
                    try:
                        print("Percentage of frames received: "+str((counter_packet/frame_num)*100))
                    except:
                        pass
                    print("Location: "+str(g.latlng[0])+","+str(g.latlng[1]))
                    print("----------------------")
                    print("------SPACECRAFT------")
                    spacecraft_data = earthmath.calculate_lookangles({
                            'lon': float(g.latlng[1]),
                            'lat': float(g.latlng[0]),
                            'alt': 0
                          }, {
                            'lon': longitude,
                            'lat': latitude,
                            'alt': altitude
                          })
                    #print(spacecraft_data)
                    print("Elevation: "+str(round(spacecraft_data['elevation'])))
                    print("Azimuth: "+str(round(spacecraft_data['azimuth'])))
                    print("Distance to spacecraft (km): "+str(float(spacecraft_data['range'])/1000))
                    print("----------------------")
                    print("==============================================================")
                    print("\n")
                packet = ""
             except Exception as e:
                print(e)
                print("ERROR: CANNOT PARSE MESSAGE :(")
                print("\n")
                packet = "" #Maybe
             except KeyboardInterrupt:
                 f.close()
                 exit()

                
             
             
    except:
        if num_nochars >= 5:
            print("WARN: NO CHARS RECEIVED...")
            num_nochars = num_nochars+1
        pass
    
