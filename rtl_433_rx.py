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
print("RTL-433/backup packet version")
time.sleep(0.5)
print("By VE3SVF")
print("\n")


#RTL-433 stuff

UDP_IP = "127.0.0.1"
UDP_PORT = 514

connected_rtl433 = True


try:
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.settimeout(0.03)
except:
    print("ERROR: CANNOT CREATE RTL-433 UDP SOCKET!")
    connected_rtl433 = False
try:
    sock.bind((UDP_IP, UDP_PORT))
except:
    print("ERROR: CANNOT CONNECT TO RTL-433 PACKET MODEM")

print("CONNECTED TO RTL-433!")

while True:
    if connected_rtl433:
        try:
            #print("RX RTL433")
            #print(connected_rtl433)
            data_RTL, addr_RTL = sock.recvfrom(1024) # buffer size is 1024 bytes
            data_RTL = data_RTL.decode()
            start = data_RTL.find("[")
            end = data_RTL.find("]")

            datafield = data_RTL[start+1:end]

            bytes_data = datafield.split(",")

            char_string = ""

            for i in range(len(bytes_data)):
                bytes_char = int_to_bytes(int(bytes_data[i]))
                char_string = char_string + bytes_char.decode('ascii')
            #print(char_string)
            print("RECEIVED PACKET FROM RTL-433!")

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
            except:
                print("Cannot parse RTL-433 packet",char_string)
            
            
            char_string = ""
        except Exception as e:
            #print(e)
            pass

