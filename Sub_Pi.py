import bluetooth
import RPi.GPIO as GPIO
#Server Adresse ['B8:27:EB:7F:76:B1']
GPIO.setmode(GPIO.BCM)
GPIO.setup(3,GPIO.OUT) # Correct with output for pump transistor
GPIO.setup(15,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(17,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(18,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)



def Soil_Hydrometry(n):
    """ Check water level for connected plants"""
    _Soil_Level = 0
    if n ==1:
        _Soil_Level = GPIO.input(15) #Input correct soil sensor
    if n ==2:
        _Soil_Level = GPIO.input(17) #Input correct soil sensor
    if n ==3:
        _Soil_Level = GPIO.input(18) #Input correct soil sensor
        
    ### Add other sensor if necessary
    return _Soil_Level

def Activate_pump(n):
    """Activate the corresponding pump"""
    #Need additionnal code for valve control
    if n==1:
        GPIO.output(3,1) # Correct with the pin of the transistor
        time.sleep(15)
    if n==2:
        GPIO.output(3,1) # Correct with the pin of the transistor
        time.sleep(15)
     if n==3:
        GPIO.output(3,1) # Correct with the pin of the transistor
        time.sleep(15)
        
#Main Loop for client
server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("",4))
server_socket.listen(1)
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
    elif "PUMP1" in data_to_receive:
        Activte_pump(1)
        data_to_send = "Watering"
    elif "PUMP2" in data_to_receive:
        Activte_pump(2)
        data_to_send = "Watering"
    elif "PUMP3" in data_to_receive:
        Activte_pump(3)
        data_to_send = "Watering"


    client_socket.send(data_to_send)

client_socket.close()
server_socket.close()

GPIO.cleanup()
