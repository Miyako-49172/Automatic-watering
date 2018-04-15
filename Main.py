#Test Documentation
import RPi.GPIO as GPIO
import bluetooth
import datetime
import time

#Client Adresse ['B8:27:EB:98:42:D1']

GPIO.setmode(GPIO.BCM)
GPIO.setup(3,GPIO.OUT) # input correct Pump Transistor command
GPIO.setup(15,GPIO.IN,pull_up_down = GPIO.PUD_DOWN) #input correct soil sensor pin
GPIO.setup(21,GPIO.OUT) 

### Function definition
def ConnectionToBluetooth(Parameter_To_Check,_client_socket):
    """ Connect to the Raspberry 0 and performe
        Either Soil hydrometry check or pump activation"""
    _client_socket.send (Parameter_To_Check)
    data = _client_socket.recv(32) #Check if the client can receive data from server
    return data

def Soil_Hydrometry(n,_client_socket):
    """ Check the water level in the plant soil"""
    _Soil_Level = 0
    if n == 0:
        _Soil_Level = GPIO.input(15) #Input correct soil sensor pin
    elif n ==1:
        _data =  ConnectionToBluetooth("SOIL1",_client_socket) #Check
        _Soil_Level = int(_data)
    return _Soil_Level

def Activate_Pump(n,_client_socket):
    """ Activate the coresponding Pump"""
    if n == 0:
        GPIO.output(3,1)# Input correct Pump transistor
        time.sleep(15)
    if n==1:
        Watering_Pump1 = ConnectionToBluetooth("PUMP1",_client_socket)
    
def Action_On_Plants_And_Updating_CSV(_File_Path,_Data_To_Write,Plant_Number):
    #Check Soil results and append them to results as well as create CSV file
    _Data_To_Write[Plant_Number].append(str(Soil_Hydrometry(Plant_Number,client_socket)))
    with open(_File_Path,'r') as _Working_File:
        FileContents = _Working_File.read() #Need to clean the whole file so that roughly one year of data remain
        _Working_File.close()
    last_watering = FileContents.splitlines()
    for Jour in range(len(last_watering)):
        if last_watering[Jour].split(',')[3] == '1':
            Date_Of_Last_Watering = datetime.datetime.strptime(last_watering[Jour].split(',')[1],"%Y-%m-%d  %H:%M")
            Time_Difference = Today - Date_Of_Last_Watering
            break

    if Time_Difference.days>2 or  Soil_Hydrometry(Plant_Number,client_socket) == 0:
        #Activate_Pump(Plant_Number,client_socket)
        Watering = '1'

    _Data_To_Write[Plant_Number].append(Watering)

    #Writting csv
    with open(_File_Path,'w') as _Working_File:
        _Working_File.seek(0)
        _Working_File.write(_Data_To_Write[Plant_Number][0])
        _Working_File.write(_Data_To_Write[Plant_Number][1])
        _Working_File.write(',')
        _Working_File.write(_Data_To_Write[Plant_Number][2])
        _Working_File.write(',')
        _Working_File.write(_Data_To_Write[Plant_Number][3])
        _Working_File.write('\n')
        _Working_File.write(FileContents)
    _Working_File.close()
    ###

                 
###Main loop
Today = datetime.datetime.today()
Time_Difference = Today
Watering = "0" #Parameter to check if we have watered today

#Initializing collected parameter
Info_Plants = [["Oranger,",Today.strftime("%Y-%m-%d  %H:%M")],["Rosier,",Today.strftime("%Y-%m-%d  %H:%M")]]
#Initializing bluetooth
client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_socket.connect(("B8:27:EB:98:42:D1",4))

#Oranger
Action_On_Plants_And_Updating_CSV('Plants_information_Oranger.csv',Info_Plants,0)
#END OF Oranger

#Rosier
Action_On_Plants_And_Updating_CSV('Plants_information_Rosier.csv',Info_Plants,1)
#END OF Rosier

print(Info_Plants[0])
GPIO.cleanup()