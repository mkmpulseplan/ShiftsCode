from pymongo import MongoClient
from bunnet import Document, init_bunnet
from pydantic import BaseModel
from typing import List
from datetime import date

class Settings(Document):
    id: str
    TwelveHourShifts: bool
    MinimumShifts: int
    ShmoneShmone: bool
    Max2ShiftsSameType: bool

def connect2DB():
        print("connecting to settings DB")
        client = MongoClient("mongodb+srv://MKM:MKM@pulseplan.11mcavy.mongodb.net/?appName=PulsePlan")
        init_bunnet(database=client.PulsePlan, document_models=[Settings])    
        return client.PulsePlan

connect2DB()
