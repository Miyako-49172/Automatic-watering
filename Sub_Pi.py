import bluetooth
import RPi.GPIO as GPIO
#Server Adresse ['B8:27:EB:7F:76:B1']
GPIO.setmode(GPIO.BCM)
GPIO.setup(3,GPIO.OUT) # Pump transistor
GPIO.setup(14,GPIO.IN,pull_up_down = GPIO.PUD_DOWN) #Mint
GPIO.setup(15,GPIO.IN,pull_up_down = GPIO.PUD_DOWN) #Strtawberry
GPIO.setup(17,GPIO.IN,pull_up_down = GPIO.PUD_DOWN) #Rose
GPIO.setup(18,GPIO.IN,pull_up_down = GPIO.PUD_DOWN) #Piment



def Soil_Hydrometry(n):
    """ Check water level for connected plants"""
    _Soil_Level = 0
    if n ==1:
        _Soil_Level = GPIO.input(15) #Input correct soil sensor
    if n ==2:
        _Soil_Level = GPIO.input(17) #Input correct soil sensor
    if n ==3:
        _Soil_Level = GPIO.input(18) #Input correct soil sensor
    if n ==4:
        _Soil_Level = GPIO.input(14) #Input correct soil sensor
        
    ### Add other sensor if necessary
    return _Soil_Level

def Activate_pump(n):
    """Activate the corresponding pump with appropriate valve
       Not available yet so depending of the distance of the plants pump longer"""
    #Need additionnal code for valve control
    if n==1:
        GPIO.output(3,1) # Correct with the pin of the transistor
        time.sleep(5)
    if n==2:
        GPIO.output(3,1) # Correct with the pin of the transistor
        time.sleep(5)
    if n==3:
        GPIO.output(3,1) # Correct with the pin of the transistor
        time.sleep(10)
    if n==4:
        GPIO.output(3,1) # Correct with the pin of the transistor
        time.sleep(10)
    GPIO.output(3,0)
        
#Main Loop for client
server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("",4))
server_socket.listen(1)
#Waiting for New connection loop

while True:
    client_socket , adress = server_socket.accept()

    while True:
        data_to_receive = str(client_socket.recv(32))
        data_to_send = "0"
#Depending on the contents of received data read sensor or activate pump
        if "SOIL1" in data_to_receive:
            data_to_send = str(Soil_Hydrometry(1))
        elif "SOIL2" in data_to_receive:
            data_to_send = str(Soil_Hydrometry(2))
        elif "SOIL3" in data_to_receive:
            data_to_send = str(Soil_Hydrometry(3))
        elif "SOIL4" in data_to_receive:
            data_to_send = str(Soil_Hydrometry(4))
        elif "PUMP1" in data_to_receive:
            Activte_pump(1)
            data_to_send = "Watering_Strawberry"
        elif "PUMP2" in data_to_receive:
            Activte_pump(2)
            data_to_send = "Watering_Rose"
        elif "PUMP3" in data_to_receive:
            Activte_pump(3)
            data_to_send = "Watering_Piment"
        elif "PUMP4" in data_to_receive:
            Activte_pump(4)
            data_to_send = "Watering_Mint"
        elif "End_Data" in data_to_receive:
            break
        client_socket.send(data_to_send)

client_socket.close()
server_socket.close()

GPIO.cleanup()

""" Test code
GPIO.setup(2,GPIO.OUT)  #Motor II A1
GPIO.setup(3,GPIO.OUT)  #Motor II A2
GPIO.setup(21,GPIO.OUT)  #Motor II B1
GPIO.setup(20,GPIO.OUT)  #Motor II B2

GPIO.setup(4,GPIO.OUT)  #Motor I A1
GPIO.setup(14,GPIO.OUT)  #Motor I A2
GPIO.setup(15,GPIO.OUT)  #Motor I B1
GPIO.setup(18,GPIO.OUT)  #Motor I B2

GPIO.setup(26,GPIO.OUT)  #Motor control 12V
GPIO.setup(19,GPIO.OUT)  #Pump Control

###Main loop

GPIO.output(26,1)
GPIO.output(19,1)

GPIO.output(2,0)
GPIO.output(3,0)
GPIO.output(20,0)
GPIO.output(21,0)
GPIO.output(4,0)
GPIO.output(14,0)
GPIO.output(15,0)
GPIO.output(18,0)

for i in range (1):
    #GPIO.output(2,1)
    #GPIO.output(3,0)
    #GPIO.output(21,1)
    #GPIO.output(20,0)
    GPIO.output(4,1)
    GPIO.output(14,0)
    GPIO.output(15,0)
    GPIO.output(18,1)
    time.sleep(30)
    #GPIO.output(2,0)
    #GPIO.output(3,1)
    #GPIO.output(21,0)
    #GPIO.output(20,1)
    GPIO.output(4,0)
    GPIO.output(14,1)
    GPIO.output(15,1)
    GPIO.output(18,0)
    time.sleep(30)
    
GPIO.output(4,0)
GPIO.output(14,0)
GPIO.output(15,0)
GPIO.output(18,0)
GPIO.output(19,0)

GPIO.cleanup()
        #GPIO.output(21,0)
        #GPIO.output(20,1)
    is closed when red si connected to B1

"""
