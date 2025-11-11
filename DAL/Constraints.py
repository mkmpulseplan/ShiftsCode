from pymongo import MongoClient
from bunnet import Document, init_bunnet
from pydantic import BaseModel
from typing import List
from datetime import date

class Filter(BaseModel):
    belongsTo: str
    startsIn: date

class Constraints(Document):
    #automatic ID
    belongsTo: str
    Contents: List[List[str]] #Prefers, Can, Prefers Not, Cannot, Unavailable
    startsIn: date 

def connect2DB():
        print("connecting to constraints DB")
        client = MongoClient("mongodb+srv://MKM:MKM@pulseplan.11mcavy.mongodb.net/?appName=PulsePlan")
        init_bunnet(database=client.PulsePlan, document_models=[Constraints])    
        return client.PulsePlan

connect2DB()