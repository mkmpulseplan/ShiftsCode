from pymongo import MongoClient
from bunnet import Document, init_bunnet
from pydantic import BaseModel
from typing import List
from datetime import date

class ChangeStatus(BaseModel):
    id: str
    new_status: str

class MoreBlockRequest(Document):
    id: str #this will be the employee who requested's name
    ExpiresIn: date
    Status: bool

def connect2DB():
        print("connecting to block requests DB")
        client = MongoClient("mongodb+srv://MKM:MKM@pulseplan.11mcavy.mongodb.net/?appName=PulsePlan")
        init_bunnet(database=client.PulsePlan, document_models=[MoreBlockRequest])    
        return client.PulsePlan

connect2DB()