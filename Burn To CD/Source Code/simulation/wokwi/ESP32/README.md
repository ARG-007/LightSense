# ESP32 Simulation

> **Model:** ESP32 DevKitC V4  
> **Code Author:** Arun R G (ARG)  

## Components Used:
- Espressif ESP32 DevkitC V4 Board
- 4 LDR Sensors with *Gamma* Slope - 0.7 and *LDR Resistance* - 50

## Networking:
- **Communication Medium:** *Wi-fi*
    - An Virtual Wifi is provided by WokWi complete with internet access
    - **Access Point Name:** Wokwi-GUEST [More Info](https://docs.wokwi.com/guides/esp32-wifi) 
- **Protocol**: *MQTT*
    - **Broker**: HiveMQ
    - **Server**: broker.mqttdashboard.com
    - **Port**: 8883 [TLS PORT], 1883 [HTTP PORT]
    - **Topic**: ABDTG_LightSense

## Instructions:
1. Goto https://wokwi.com/projects/new/esp32  
2. copy & paste content within [diagram.json](diagram.json) to diagram.json in the online Editor
3. Do Only one of the following based on your language preference:  
    - **Micropython** : Copy & Paste Content within [main.py](main.py) to main.py in the editor 
        > (if no file named ***main.py*** present create one using **dropdown** button)
    - **Arduino C++ Like** : Copy & Paste Content within [sketch.ino](sketch.ino) to sketch.ino in the editor 
        > (if no file named sketch.ino present create one using **dropdown** button)  
    > ***Delete the opposing language file as their presence can affect the execution***
4. Run Simulation by clicking the **Play** Button present on top left corner under the simulation tab.
5. To change the Luminance value click on one of the LDR Sensor and drag the slider to desired value
6. This Simulation uses MQTT (A PubSub Protocol) to publish updates to the clients, to manually view the messages follow these instructions :
    - Go to http://www.hivemq.com/demos/websocket-client/
    - Click "Connect"
    - Under Subscriptions, click "Add New Topic Subscription"
    - In the Topic field, type "ABDTG_LightSense" then click "Subscribe"

## Limitation
Wokwi cannot simulate Light, hence LDR Sensor works only through manual modification, which makes it impossible to create a automated test bed within simulation.