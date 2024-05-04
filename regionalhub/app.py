from turtle import title
import customtkinter as ctk
from mysql.connector import MySQLConnection
from mysql.connector.cursor import *
from data import Sensor, SensorState
from tkintermapview import TkinterMapView
from PIL import ImageTk, Image
import os

from datamanager import MQTT

ctk.set_appearance_mode("dark")

current_path= os.path.join(os.path.dirname(os.path.abspath(__file__)))

STATE_COLORS = ["green", "orange", "red"]

class SensorButton(ctk.CTkFrame):
    def __init__(self, master, sensor: Sensor,on_click, **kwargs):
        super().__init__(master, **kwargs)
        self.data:Sensor = sensor

        self.inactive_color = "grey"
        self.hover_color = "darkgrey"

        self.configure(fg_color=self.inactive_color)

        self.nameLabel: ctk.CTkLabel = ctk.CTkLabel(self, text=f"Street Light : {sensor.id}",corner_radius=10, bg_color=self.inactive_color)
        self.stateLabel: ctk.CTkLabel = ctk.CTkLabel(self, corner_radius=10, width=30, height=10, text="", bg_color=self.inactive_color)
        self.nameLabel.grid(row=0, column=0, padx=10, pady=10)
        self.stateLabel.grid(row=0, column=1, padx=10, pady=10)
        self.updatestate()

        self.bind("<Enter>", self.onHover)
        self.nameLabel.bind("<Enter>", self.onHover)
        self.stateLabel.bind("<Enter>", self.onHover)

        self.bind("<Leave>", self.onLeave)
        self.nameLabel.bind("<Leave>", self.onLeave)
        self.stateLabel.bind("<Leave>", self.onLeave)

        self.bind("<Button-1>", lambda x : on_click(sensor.id))
        self.nameLabel.bind("<Button-1>", lambda x : on_click(sensor.id))
        self.stateLabel.bind("<Button-1>", lambda x : on_click(sensor.id))



    def updatestate(self):
        self.stateLabel.configure(fg_color = STATE_COLORS[self.data.state-1])

    def onHover(self, event):
        self.configure( fg_color=self.hover_color)
        self.nameLabel.configure(bg_color=self.hover_color)
        self.stateLabel.configure(bg_color=self.hover_color)

    def onLeave(self, event):
        self.configure( fg_color=self.inactive_color)
        self.nameLabel.configure(bg_color=self.inactive_color)
        self.stateLabel.configure(bg_color=self.inactive_color)


class App(ctk.CTk):
    NAME = "Regional HUB Debug Portal"
    MWIDTH = 800
    MHEIGHT = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(App.NAME)
        self.geometry(f"{App.MWIDTH}x{App.MHEIGHT}")
        self.minsize(App.MWIDTH, App.MHEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.db = MySQLConnection(username="lightsense", password="ABDGT", database="LightSense")
        self.mqtt = MQTT(self.on_message)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.left_tab = ctk.CTkTabview(self)
        self.left_tab.grid(row=0,column=0, sticky="nswe") 
        self.left_tab.add("Map")
        # self.left_tab.add("Graph")
        self.left_tab.tab("Map").grid_columnconfigure(0, weight=1)
        self.left_tab.tab("Map").grid_rowconfigure(0, weight=1)
        # self.left_tab.tab("Graph").grid_columnconfigure(0, weight=1)
        # self.left_tab.tab("Graph").grid_rowconfigure(0, weight=1)
        
        self.map_widget = TkinterMapView(self.left_tab.tab("Map"))
        self.map_widget.grid(row=0, column=0, sticky="nsew")
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

        self.sensorList = ctk.CTkScrollableFrame(self, label_text="Sensors", width=200)
        self.sensorList.grid_columnconfigure(0, weight=1, pad=3)
        self.sensorList.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.STATE_ICON = [
            ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "working.png")).resize((50, 50))),
            ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "sleeping.png")).resize((50, 50))),
            ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "fault.png")).resize((50, 50))),
            ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "selected_working.png")).resize((50, 50))),
            ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "selected_sleeping.png")).resize((50, 50))),
            ImageTk.PhotoImage(Image.open(os.path.join(current_path, "images", "selected_faulty.png")).resize((50, 50))),

        ]

        self.sensor_data={}
        self.sensor_buttons = {}
        self.sensor_location_markers = {}

        cursor= self.db.cursor(buffered=True)
        cursor.execute("SELECT id, state, ST_X(coords) AS lt,ST_Y(coords) AS lg, updated_on FROM StreetLight")
        for i, sensor in enumerate(cursor.fetchall()):
            temp_s = Sensor(*sensor)
            self.sensor_data[temp_s.id] = temp_s
            sb = SensorButton(self.sensorList, temp_s, on_click=self.focusSensor, corner_radius=10)
            sb.grid(row=i, column=0, sticky="nsew",pady=5)
            self.sensor_buttons[temp_s.id] = sb
            
            self.sensor_location_markers[temp_s.id] = self.map_widget.set_marker(temp_s.cx, temp_s.cy,icon=self.STATE_ICON[temp_s.state-1])
        
        self.focused = 1
        self.map_widget.set_position(self.sensor_data[1].cx, self.sensor_data[1].cy)

        self.mqtt.loop_start()


    def focusSensor(self, sensorId):
        marker = self.sensor_location_markers[self.focused]
        marker.change_icon(self.STATE_ICON[self.sensor_data[sensorId].state-1])
        self.map_widget.set_position(self.sensor_data[sensorId].cx, self.sensor_data[sensorId].cy)
        self.focused = sensorId
        marker = self.sensor_location_markers[self.focused]
        marker.change_icon(self.STATE_ICON[self.sensor_data[sensorId].state+2])
        self.map_widget.set_zoom(20)

    def on_message(self, data):
        sensor = self.sensor_data[data.id]
        sensor.state = data.state
        self.sensor_buttons[data.id].updatestate()
        self.sensor_location_markers[data.id].change_icon(self.STATE_ICON[(data.state-1)+(2*(self.focused==data.id))])
        
    def on_closing(self, event=0):
        self.mqtt.loop_stop()
        self.db.close()
        self.destroy()
    

app = App()

app.mainloop()

