from pymongo import MongoClient
from bunnet import Document, init_bunnet
from pydantic import BaseModel

class SupportQuery(Document):
    #automatic ID
    From: str
    Subject: str
    Contents: str
    isPending: bool

def connect2DB():
        print("connecting to support DB")
        client = MongoClient("mongodb+srv://MKM:MKM@pulseplan.11mcavy.mongodb.net/?appName=PulsePlan")
        init_bunnet(database=client.PulsePlan, document_models=[SupportQuery])    
        return client.PulsePlan

connect2DB()