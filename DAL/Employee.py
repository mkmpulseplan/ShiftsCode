from pymongo import MongoClient
from bunnet import Document, init_bunnet
from pydantic import BaseModel


class Login(BaseModel):
      id: str
      password: str

class New(BaseModel):
      id: str
      lastName: str
      password: str

class Employee(Document):
    id: str #This is will be employee's first name
    lastName: str
    password: str
    isApproved: bool
    isHidden: bool
    isManager: bool
    isDev: bool
    isLastResort: bool
    isNationalService: bool
    NeverBreak88: bool


def connect2DB():
        print("connecting to employee DB")
        client = MongoClient("mongodb+srv://MKM:MKM@pulseplan.11mcavy.mongodb.net/?appName=PulsePlan")
        init_bunnet(database=client.PulsePlan, document_models=[Employee])    
        return client.PulsePlan

connect2DB()