from turtle import width
from typing import Dict
from paho.mqtt import client as mqttc
import customtkinter
import json


class LDR(customtkinter.CTkFrame):
    def __init__(self, master, id, status = True, **kwargs):
        super().__init__(master, **kwargs)
        self.id = id
        self.status = status
        self.nameLabel: customtkinter.CTkLabel = customtkinter.CTkLabel(self, text=id)
        self.stateLabel: customtkinter.CTkLabel = customtkinter.CTkLabel(self, corner_radius=10, text_color="white")
        self.nameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.stateLabel.grid(row=0, column=1, padx=10, pady=10)
        self.refresh_status()

    def set_status(self, status: bool):
        self.status = status
        self.refresh_status()

    def refresh_status(self):
        if self.status:
            self.stateLabel.configure(text="Working", fg_color="green")
        else:
            self.stateLabel.configure(text="Not Working", fg_color="red")

class StatusFrame(customtkinter.CTkFrame):
    def __init__(self, master, ldr_list= [], **kwargs):
        super().__init__(master, **kwargs)
        self.ldrs:Dict[str, LDR] = {}
        self.ldr_count = 0
        # self.grid_columnconfigure(0, weight=1)
        
        for i in ldr_list:
            self.add_ldr(i)    
    
    def add_ldr(self, ldr_id, inital_status=True):
        ldr = LDR(self, ldr_id, inital_status)
        ldr.grid(row = self.ldr_count, column=0)
        self.ldr_count+=1
        self.ldrs[ldr_id] = ldr
    
    def get(self, id):
        return self.ldrs[id]

    def set_ldr_status(self, id, status):
        self.ldrs[id].set_status(status)
    

app: customtkinter.CTk = customtkinter.CTk()
app.title("LigthSense Debug Portal")
app.grid_columnconfigure(0, weight=1)
LDR_SENSORS = ["LDR1111", "LDR1112", "LDR1113", "LDR1114"]
ldr_panel: StatusFrame = StatusFrame(app, LDR_SENSORS, width=500)
ldr_panel.grid(row=0, column=0)
# def createFrame(name: str, master: customtkinter.CTk):
#     frame = customtkinter.CTkFrame(master)
#     nameLabel = customtkinter.CTkLabel(frame,text=name)
#     nameLabel.grid(row = 0, column=0, padx=10, pady=10)
#     stateLabel = customtkinter.CTkLabel(frame, text="working", fg_color="green", corner_radius=10, text_color="white")
#     stateLabel.grid(row = 0, column=1, padx=10, pady=10)
#     return [frame, nameLabel, stateLabel]

# ldr = {}
# for j,i in enumerate(LDR_SENSORS):
#     ldr[i] = LDR(app,i)
#     ldr[i].grid(row=j,column=0)

TOPIC = "ABDTG_LightSense"
PORT = 1883
SERVER = "broker.mqttdashboard.com"

def on_connect(client: mqttc.Client, userdata, flags: mqttc.ConnectFlags, reason_code: mqttc.ReasonCode, properties ):
    print("MQTT Connection Response Received ")
    print(f"\t{client=}")
    print(f"\t{userdata=}")
    print(f"\t{flags=}")
    print(f"\t{reason_code=}")
    print(f"\t{properties=}")
    if(reason_code.is_failure):
        print("MQTT Server Failed To Connect")
    else:
        client.subscribe(TOPIC)

def on_subscribe(client, userdata, mid, reason_code_list, properties):
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")

def on_message(client, userdata, message):
    payload:dict = json.loads(message.payload)
    for name,status in payload.items():
        ldr_panel.get(name).set_status(status.upper()=="WORKING")
    print(payload)

MQTTC = mqttc.Client(mqttc.CallbackAPIVersion.VERSION2, protocol=mqttc.MQTTv5)


MQTTC.on_connect = on_connect
MQTTC.on_subscribe = on_subscribe
MQTTC.on_message = on_message


print("Connecting to MQTT Server")

MQTTC.connect(SERVER, PORT)

MQTTC.loop_start()

app.mainloop()

MQTTC.loop_stop()


