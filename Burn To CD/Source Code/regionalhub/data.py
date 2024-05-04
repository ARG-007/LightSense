from datetime import datetime
from enum import IntEnum

class SensorState(IntEnum):
    WORKING = 1
    SLEEPING = 2
    FAULT = 3

class SensorData:
    def __init__(self, id=0, lamp=0, env=0, state=0, timestamp=0):
        self.id: int = id
        self.lamp: int= lamp
        self.env:int = env
        self.state:int = state
        self.timestamp:datetime = datetime.now()
    
    @staticmethod
    def unpack(masked):
        data = SensorData()
        data.state = masked & 3
        masked >>= 2
        data.env = masked & 1023
        masked >>=10
        data.lamp = masked & 1023
        masked >>=10
        data.id = masked
        return data
    
    def __iter__(self):
        yield self.id
        yield self.state
        yield self.lamp
        yield self.env
        yield self.timestamp
    
    def __repr__(self):
        return f"ID: {self.id!r}, Lamp: {self.lamp!r}, Environment: {self.env!r}, State: {self.state!r}, Timestamp: {self.timestamp!r}"
    
class Sensor:
    def __init__(self, id: int, state: int, cx: float, cy:float,  last_updated:datetime):
        self.id = id
        self.state =state
        self.cx = cx
        self.cy = cy
        self.last_updated = last_updated
