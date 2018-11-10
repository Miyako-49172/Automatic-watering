#Test Documentation
import RPi.GPIO as GPIO
import bluetooth
import datetime
import time
import shutil

#Client Adresse ['B8:27:EB:98:42:D1']

GPIO.setmode(GPIO.BCM)
GPIO.setup(15,GPIO.IN,pull_up_down = GPIO.PUD_DOWN) #Soil sensor pin
GPIO.setup(21,GPIO.OUT)  #Pump Controller Pin

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
    elif n ==2:
        _data =  ConnectionToBluetooth("SOIL2",_client_socket) #Check
        _Soil_Level = int(_data)
    elif n ==3:
        _data =  ConnectionToBluetooth("SOIL3",_client_socket) #Check
        _Soil_Level = int(_data)
    elif n ==4:
        _data =  ConnectionToBluetooth("SOIL4",_client_socket) #Check
        _Soil_Level = int(_data)
    return _Soil_Level

def Activate_Pump(n,_client_socket):
    """ Activate the coresponding Pump"""
    if n == 0:
        GPIO.output(21,1)
        time.sleep(10)
        GPIO.output(21,0)
    if n==1:
        Watering_Pump1 = ConnectionToBluetooth("PUMP1",_client_socket)
    if n==2:
        Watering_Pump1 = ConnectionToBluetooth("PUMP2",_client_socket)
    if n==3:
        Watering_Pump1 = ConnectionToBluetooth("PUMP3",_client_socket)
    if n==4:
        Watering_Pump1 = ConnectionToBluetooth("PUMP4",_client_socket)
        
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

    Watering = "0" #Parameter to check if we have watered today
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

#Initializing collected parameter
Info_Plants = [["Oranger,",Today.strftime("%Y-%m-%d  %H:%M")],["Basil,",Today.strftime("%Y-%m-%d  %H:%M")],["Rosier,",Today.strftime("%Y-%m-%d  %H:%M")],["Menthe,",Today.strftime("%Y-%m-%d  %H:%M")],["Aubergine,",Today.strftime("%Y-%m-%d  %H:%M")]]
#Initializing bluetooth
client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_socket.connect(("B8:27:EB:98:42:D1",4))

#Oranger
Action_On_Plants_And_Updating_CSV('/home/pi/Program/Plants_information_Oranger.csv',Info_Plants,0,client_socket)
shutil.copy2('/home/pi/Program/Plants_information_Oranger.csv','/var/plant_log/Plants_information_Oranger.csv')
#END OF Oranger
time.sleep(15)

#Basil
Action_On_Plants_And_Updating_CSV('/home/pi/Program/Plants_information_Basil.csv',Info_Plants,1,client_socket)
shutil.copy2('/home/pi/Program/Plants_information_Basil.csv','/var/plant_log/Plants_information_Basil.csv')
#END OF Basil
time.sleep(15)
#Rosier
Action_On_Plants_And_Updating_CSV('/home/pi/Program/Plants_information_Rosier.csv',Info_Plants,2,client_socket)
shutil.copy2('/home/pi/Program/Plants_information_Rosier.csv','/var/plant_log/Plants_information_Rosier.csv')
#END OF Rosier
time.sleep(15)
#Menthe
Action_On_Plants_And_Updating_CSV('/home/pi/Program/Plants_information_Menthe.csv',Info_Plants,3,client_socket)
shutil.copy2('/home/pi/Program/Plants_information_Menthe.csv','/var/plant_log/Plants_information_Menthe.csv')
#END OF Menthe
time.sleep(15)
#Eggplant
Action_On_Plants_And_Updating_CSV('/home/pi/Program/Plants_information_Aubergine.csv',Info_Plants,4,client_socket)
shutil.copy2('/home/pi/Program/Plants_information_Aubergine.csv','/var/plant_log/Plants_information_Aubergine.csv')
#END OF Eggplant
time.sleep(15)
#print(Info_Plants[0])
GPIO.cleanup()
client_socket.send("End_Data")
