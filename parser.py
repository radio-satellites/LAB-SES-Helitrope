def parse_string(string):
    parameters = string.split(",")
    num_correct = 0
    try:
        pressure = float(parameters[1]) #Recover the data back
        if pressure > 0 and pressure < 20000:
            num_correct = num_correct+1
        else:
            pressure = 0
    except:
        pressure = 0
    try:
        altitude = float(parameters[2])
        if altitude > 0 and altitude < 40000:
            num_correct = num_correct+1
        else:
            altitude = 0
    except:
        altitude = 0
    try:
        temperature = float(parameters[3])
        num_correct = num_correct+1
    except:
        temperature = 0
    try:
        latitude = float(parameters[4])/1000000
        if latitude > 20 and latitude < 100:
            num_correct = num_correct+1
        else:
            latitude = 0
            
    except:
        latitude = 0
    try:
        longitude = float(parameters[5])/-1000000
        if longitude < -10 and longitude > -100:
            num_correct = num_correct+1
        else:
            longitude = 0
    except:
        longitude = 0
    try:
        frame_num = int(parameters[6])
        if frame_num < 0:
            frame_num = 0
    except:
        frame_num = 0
        
    if num_correct > 0:
        return pressure,altitude,temperature,latitude,longitude,frame_num
    else:
        return 0

def parse_shortform(data):
    parameters = data.split("?")
    num_correct = 0
    try:
        latitude = float(parameters[0])/1000000
        if latitude > 20 and latitude < 100:
            num_correct = num_correct+1
        else:
            latitude = 0
            
    except:
        latitude = 0
    try:
        longitude = float(parameters[1])/-1000000
        if longitude < -10 and longitude > -100:
            num_correct = num_correct+1
        else:
            longitude = 0
    except:
        longitude = 0
    try:
        altitude = float(parameters[2])
        num_correct = num_correct+1
    except:
        altitude = 0

    return latitude,longitude,altitude
