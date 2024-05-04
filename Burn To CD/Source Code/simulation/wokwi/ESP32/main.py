# ESP32 Micropython 

import network
import time
from machine import Pin,ADC
import json
from umqtt.simple import MQTTClient


# Connecting to a WLAN network[specifically WokWi Virtual Wifi]
print("="*80,"\nConnecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print("\nWifi Connected\n",'-'*80)

# Setting Up MQTT Connection
print("Connecting to MQTT Broker on Following Parameters :\n",'-'*80)
mqtt_params = {
    'client_id':'ABDTG_LS_ESP32PUB',
    'server':'broker.mqttdashboard.com',
    'user':'',
    'password':''
}
print(f"Client_ID: {mqtt_params['client_id']}\nServer: {mqtt_params['server']}")

MQTT_TOPIC = 'ABDTG_LightSense'
print(f"On Topic: {MQTT_TOPIC}\n{'-'*80}")
publisher = MQTTClient(**mqtt_params)
publisher.connect()

print("Connection Successfull\n","="*80)

#Setup LDR Sensor
class LDR:
  GAMMA = 0.7
  RL10 = 50e3
  THERSHOLD = 400
  def __init__(self, pin):
    self.pin = pin
    self.port = ADC(Pin(pin))
    # Set max readable voltage to 3.3V
    self.port.atten(ADC.ATTN_11DB)
  
  def convert_lux(self, value):
    resistance = 10e3* (value / (4095 - value))
    return 10 * pow(self.RL10/resistance, 1/self.GAMMA)

  def read(self):
    return self.convert_lux(self.port.read())

  def status(self):
    return "WORKING" if self.read()>=self.THERSHOLD else "FAULT"
  
  def __str__(self):
    return self.status()
  
# Setup Inputs 
LDR_1 = LDR(32)
LDR_2 = LDR(33)
LDR_3 = LDR(34)
LDR_4 = LDR(35)

LDR_UPDATE = {'LDR1111': LDR_1, 'LDR1112': LDR_2, 'LDR1113': LDR_3, 'LDR1114': LDR_4}



print("Reading LDR Sensor Values")
while True:
  print(f"LDR Sensor 1[Pin {LDR_1.pin}]: {LDR_1.read()}, {LDR_1}")
  print(f"LDR Sensor 2[Pin {LDR_2.pin}]: {LDR_2.read()}, {LDR_2}")
  print(f"LDR Sensor 3[Pin {LDR_3.pin}]: {LDR_3.read()}, {LDR_3}")
  print(f"LDR Sensor 4[Pin {LDR_4.pin}]: {LDR_4.read()}, {LDR_4}")
  publisher.publish(MQTT_TOPIC, json.dumps({i:j.__str__() for i,j in LDR_UPDATE.items()}))
  time.sleep(1)



