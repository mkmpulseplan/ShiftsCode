from pymongo import MongoClient
from bunnet import Document, init_bunnet
from pydantic import BaseModel
from typing import List
from DAL.Shift import *

class SwitchRequest(Document):
    #automatic ID
    From: str
    to: str
    FromShiftID: str
    ToShiftID: str
    ManagerStatus: str
    EmployeeStatus: str

def connect2DB():
        print("connecting to switch requests DB")
        client = MongoClient("mongodb+srv://MKM:MKM@pulseplan.11mcavy.mongodb.net/?appName=PulsePlan")
        init_bunnet(database=client.PulsePlan, document_models=[SwitchRequest])    
        return client.PulsePlan

connect2DB()