import serial
from paho.mqtt import client as mqttc
from time import sleep
from pprint import pprint
import re

SERVER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "ABDTG_LightSense"

MQTTC = mqttc.Client(mqttc.CallbackAPIVersion.VERSION2, protocol=mqttc.MQTTv5)
MQTTC.connect(SERVER, PORT)

aurdino_connection = serial.Serial("COM14", 115200)

def extract_hexcode(data):
    hexcode_match = re.search(r'Hex Data: ([0-9A-Fa-f]+)', data)
    if hexcode_match:
        return hexcode_match.group(1)
    return None


try:
    while True:
        # Read serial data line by line
        line = aurdino_connection.readline().decode().strip()
        

        print(line)
        # Check if line matches expected format
        if line.startswith("Hex Data: "):
            hexcode = extract_hexcode(line)
            if hexcode:
                # Publish hexcode to MQTT topic
                print("Publishing hexdata:", hexcode)
                MQTTC.publish(TOPIC, hexcode)

except serial.SerialException as e:
    print("Serial port error:", e)

finally:
    aurdino_connection.close()  # Close serial port
    MQTTC.disconnect() 