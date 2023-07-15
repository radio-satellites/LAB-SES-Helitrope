import collections

def return_cyclic_buffer(ob):
    return list(ob)

def return_cyclic_buffer_string(ob):
    return ''.join(return_cyclic_buffer(ob))

def find_sync(syncword,data):
    d = collections.deque(maxlen=len(syncword))
    correlation_co = []

    #create correlation arrays and a circular buffer!

    for i in range(len(syncword)):
        d.append(data[i])
        
    correlation_co.append(correlate(syncword,return_cyclic_buffer_string(d)))

    #now, the buffer has the INITIAL STATE, that is, the first few characaters with length in total equal to the buffer size (length of the syncword). 
    
    for i in range(len(data)-len(syncword)): #-len(syncword) because we already appended the first few characters (see above)!
        d.append(data[i+len(syncword)]) #same reason as above
        correlation_co.append(correlate(syncword,return_cyclic_buffer_string(d)))

    #find highest correlation coeffecient
    co = max(correlation_co)
        

    co_position = correlation_co.index(co)

    if co == 0:
        co_position = None

    return co_position
            

def correlate(one,two):
    correlation = 0
    
    if len(str(one)) != len(str(two)):
        print("Length is not the same")
        return 0
    for i in range(len(str(one))):
        char_1 = str(one)[i]
        char_2 = str(two)[i]

        if str(char_1) == str(char_2):
            correlation = correlation + 1
        else:
            pass
    return correlation
