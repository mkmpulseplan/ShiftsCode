from pymongo import MongoClient
from bunnet import Document, init_bunnet
from pydantic import BaseModel
from typing import List
from datetime import date

class VacationRequest(Document):
    #automatic ID
    belongsTo: str
    startsIn: date
    endsIn: date
    Status: str



def connect2DB():
        print("connecting to vacation requests DB")
        client = MongoClient("mongodb+srv://MKM:MKM@pulseplan.11mcavy.mongodb.net/?appName=PulsePlan")
        init_bunnet(database=client.PulsePlan, document_models=[VacationRequest])    
        return client.PulsePlan

connect2DB()

