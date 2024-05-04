import serial
from paho.mqtt import client as mqttc
from time import sleep

SERVER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "ABDTG_LightSense"

MQTTC = mqttc.Client(mqttc.CallbackAPIVersion.VERSION2, protocol=mqttc.MQTTv5)
MQTTC.connect(SERVER, PORT)

aurdino_connection = serial.Serial("/dev/ttyUSB0", 115200)

while True:
    if(aurdino_connection.in_waiting() > 0):
        log = aurdino_connection.readlines()