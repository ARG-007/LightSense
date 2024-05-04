from datetime import datetime
from pip._vendor.rich.pretty import pprint
from paho.mqtt import client as mqttc
from mysql.connector import MySQLConnection
from data import SensorData

SENSOR_DATA_INSERT= "INSERT INTO SensorData VALUE(?,?,?,?,?)"

SERVER = "broker.mqttdashboard.com"
PORT = 1883
TOPIC = "ABDTG_LightSense"

class MQTT:
    def __init__(self, callback):  
        self.callback = callback

        self.MQTTC = mqttc.Client(mqttc.CallbackAPIVersion.VERSION2, protocol=mqttc.MQTTv5)
        self.sqlconnecter = MySQLConnection(username="lightsense", password="ABDGT", database="LightSense")

        self.MQTTC.on_connect = self.on_connect
        self.MQTTC.on_subscribe = self.on_subscribe
        self.MQTTC.on_message = self.on_message

        self.MQTTC.connect(SERVER, PORT)

    def on_connect(self, client: mqttc.Client, userdata, flags: mqttc.ConnectFlags, reason_code: mqttc.ReasonCode, properties ):
        print("MQTT Connection Response Received ")
        pprint(f"{userdata=}")
        pprint(f"{flags=}")
        pprint(f"{reason_code=}")
        pprint(f"{properties=}")
        if(reason_code.is_failure):
            print("MQTT Server Failed To Connect")
        else:
            client.subscribe(TOPIC)

    def on_subscribe(self, client, userdata, mid, reason_code_list, properties):
        if reason_code_list[0].is_failure:
            print(f"Broker rejected you subscription: {reason_code_list[0]}")
        else:
            print(f"Broker granted the following QoS: {reason_code_list[0].value}")

    def on_message(self, client, userdata, message):
        data:SensorData = SensorData.unpack(int(message.payload.decode('utf-8'),16))
        pprint(data)
        cursor = self.sqlconnecter.cursor(prepared=True)
        cursor.execute(SENSOR_DATA_INSERT, tuple(data))
        if(data.state==3):
            cursor.execute("SELECT id FROM Repair_Assignment WHERE light_id=? AND task_state='ASSIGNED'",(data.id,))
            if(len(cursor.fetchall())==0):
                cursor.close()
                cursor = self.sqlconnecter.cursor(buffered=True)
                cursor.callproc("Assign_Technician_With_MinWork", (data.id,))
        cursor.fetchall()
        cursor.close()
        self.sqlconnecter.commit()
        self.callback(data)

    def loop_start(self):
        self.MQTTC.loop_start()

    def loop_stop(self):
        self.MQTTC.loop_stop()




