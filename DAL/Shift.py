from pymongo import MongoClient
from bunnet import Document, init_bunnet
from pydantic import BaseModel
from typing import List
from datetime import date
      
class Filter(BaseModel):
      Date: date
      Type: str

class Switches(BaseModel):
    shift1: str
    shift2: str
    
class Shift(Document):
    #automatic ID
    belongsTo: str
    Date: date
    Day: str
    Type: str




def connect2DB():
        print("connecting to shift DB")
        client = MongoClient("mongodb+srv://MKM:MKM@pulseplan.11mcavy.mongodb.net/?appName=PulsePlan")
        init_bunnet(database=client.PulsePlan, document_models=[Shift])    
        return client.PulsePlan

connect2DB()