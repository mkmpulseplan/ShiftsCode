from pymongo import MongoClient
from bunnet import Document, init_bunnet
from pydantic import BaseModel
from typing import List
from datetime import date
from DAL.Shift import *
from DAL.Constraints import * 
      
class Schedule(Document):
    #automatic ID
    startsIn: date
    ShiftsSTR: List[List[str]]
    Shifts: List[List[Shift]]


def connect2DB():
        print("connecting to schedule DB")
        client = MongoClient("mongodb+srv://MKM:MKM@pulseplan.11mcavy.mongodb.net/?appName=PulsePlan")
        init_bunnet(database=client.PulsePlan, document_models=[Schedule])    
        return client.PulsePlan

connect2DB()