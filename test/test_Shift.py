import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI,status
from fastapi.testclient import TestClient
from main import app
from  DAL.Employee import * 
import random
from pydantic import TypeAdapter
from datetime import date, timedelta

client = TestClient(app)

#create a data object for employee creation
def create_employee():
    random_int = random.randint(0,100000000000)
    id = "test_"+str(random_int)
    lastName = "XxX"
    password = "test123"
    data = {'id': id, "lastName": lastName, "password": password}
    return data

#test adding a shift
def test_add():
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    data = {'belongsTo': response1.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Evening"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['belongsTo']==data['belongsTo']
    assert response.json()['Date']==data['Date']
    assert response.json()['Day']==data['Day']
    assert response.json()['Type']==data['Type']
    #try to create a shift with the same type and date, expects to delete the 1st one and create new
    response2 = client.post("/shift/add", json=data)
    assert response2.json()['_id']!=response.json()['_id']
    data = {'Date':response2.json()['Date'], 'Type':response2.json()['Type']}
    response = client.post("/shift/by_date_and_type", json=data)
    assert response.json()['_id']==response2.json()['_id']

#test switch function
def test_switch():
    #create employees
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    data = create_employee()
    response2 = client.post("/employee/add", json = data)
    assert response2.status_code == status.HTTP_200_OK
    #create shifts
    data = {'belongsTo': response1.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Evening"}
    response3 = client.post("/shift/add", json=data)
    assert response3.status_code == status.HTTP_200_OK
    data = {'belongsTo': response2.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Morning"}
    response4 = client.post("/shift/add", json=data)
    assert response4.status_code == status.HTTP_200_OK
    #switch
    data = {'shift1':response3.json(), 'shift2':response4.json()}
    response = client.put("/shift/Switch", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'Date':response3.json()['Date'], 'Type':response3.json()['Type']}
    response = client.post("/shift/by_date_and_type", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id']==response3.json()['_id']
    assert response.json()['belongsTo']==response4.json()['belongsTo']
    data = {'Date':response4.json()['Date'], 'Type':response4.json()['Type']}
    response = client.post("/shift/by_date_and_type", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id']==response4.json()['_id']
    assert response.json()['belongsTo']==response3.json()['belongsTo']
    #delete 1 employee, expect to get 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    data = {'shift1':response3.json(), 'shift2':response4.json()}
    response = client.put("/shift/Switch", json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

#test finding all shifts
def test_findAll():
    #create employees
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    data = create_employee()
    response2 = client.post("/employee/add", json = data)
    assert response2.status_code == status.HTTP_200_OK
    data = create_employee()
    response3 = client.post("/employee/add", json = data)
    assert response3.status_code == status.HTTP_200_OK
    #create shifts
    data = {'belongsTo': response1.json()['_id'], 'Date':(date.today()+timedelta(days=2)).isoformat(), 'Day':(date.today()+timedelta(days=2)).strftime("%A"), 'Type': "Evening"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response1.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Morning"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response2.json()['_id'], 'Date':(date.today()+timedelta(days=2)).isoformat(), 'Day':(date.today()+timedelta(days=2)).strftime("%A"), 'Type': "Night"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response3.json()['_id'], 'Date':(date.today()+timedelta(days=3)).isoformat(), 'Day':(date.today()+timedelta(days=3)).strftime("%A"), 'Type': "Night"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    
    response4 = client.get("/shift/all")
    assert response4.status_code == status.HTTP_200_OK
    count = len(response4.json())
    #delete a shift, make sure the count is down
    response5 = client.delete("/shift/delete/"+response.json()['_id'])
    assert response5.status_code == status.HTTP_200_OK
    response4 = client.get("/shift/all")
    assert response4.status_code == status.HTTP_200_OK
    assert len(response4.json())==count-1

#test finding by employee
def test_findByEmployee():
    #create employees
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    data = create_employee()
    response2 = client.post("/employee/add", json = data)
    assert response2.status_code == status.HTTP_200_OK
    data = create_employee()
    response3 = client.post("/employee/add", json = data)
    assert response3.status_code == status.HTTP_200_OK
    #create shifts
    data = {'belongsTo': response1.json()['_id'], 'Date':(date.today()+timedelta(days=2)).isoformat(), 'Day':(date.today()+timedelta(days=2)).strftime("%A"), 'Type': "Evening"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response1.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Morning"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response2.json()['_id'], 'Date':(date.today()+timedelta(days=2)).isoformat(), 'Day':(date.today()+timedelta(days=2)).strftime("%A"), 'Type': "Night"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response3.json()['_id'], 'Date':(date.today()+timedelta(days=3)).isoformat(), 'Day':(date.today()+timedelta(days=3)).strftime("%A"), 'Type': "Night"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK

    response4 = client.get("/shift/all_by_employee/"+response1.json()['_id'])
    assert response4.status_code == status.HTTP_200_OK
    for S in response4.json():
        assert S['belongsTo']==response1.json()['_id']

#test finding by date 
def test_findByDate():
    #create employees
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    data = create_employee()
    response2 = client.post("/employee/add", json = data)
    assert response2.status_code == status.HTTP_200_OK
    data = create_employee()
    response3 = client.post("/employee/add", json = data)
    assert response3.status_code == status.HTTP_200_OK
    #create shifts
    data = {'belongsTo': response1.json()['_id'], 'Date':(date.today()+timedelta(days=2)).isoformat(), 'Day':(date.today()+timedelta(days=2)).strftime("%A"), 'Type': "Evening"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response1.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Morning"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response2.json()['_id'], 'Date':(date.today()+timedelta(days=2)).isoformat(), 'Day':(date.today()+timedelta(days=2)).strftime("%A"), 'Type': "Night"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response3.json()['_id'], 'Date':(date.today()+timedelta(days=3)).isoformat(), 'Day':(date.today()+timedelta(days=3)).strftime("%A"), 'Type': "Night"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    
    response4 = client.get("/shift/all_by_date/"+(date.today()+timedelta(days=2)).isoformat())
    assert response4.status_code == status.HTTP_200_OK
    assert len(response4.json())<=3
    for S in response4.json():
        assert S['Date']==(date.today()+timedelta(days=2)).isoformat()

#test finding by both date and type
def test_findByDateAndType():
    #create employees
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    data = create_employee()
    response2 = client.post("/employee/add", json = data)
    assert response2.status_code == status.HTTP_200_OK
    data = create_employee()
    response3 = client.post("/employee/add", json = data)
    assert response3.status_code == status.HTTP_200_OK
    #create shifts
    data = {'belongsTo': response1.json()['_id'], 'Date':(date.today()+timedelta(days=2)).isoformat(), 'Day':(date.today()+timedelta(days=2)).strftime("%A"), 'Type': "Evening"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response1.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Morning"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response2.json()['_id'], 'Date':(date.today()+timedelta(days=2)).isoformat(), 'Day':(date.today()+timedelta(days=2)).strftime("%A"), 'Type': "Night"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response3.json()['_id'], 'Date':(date.today()+timedelta(days=3)).isoformat(), 'Day':(date.today()+timedelta(days=3)).strftime("%A"), 'Type': "Night"}
    response = client.post("/shift/add", json=data)
    assert response.status_code == status.HTTP_200_OK

    data = {'Date': (date.today()+timedelta(days=2)).isoformat(),'Type': "Evening"}
    response4 = client.post("/shift/by_date_and_type", json=data)
    assert response4.status_code==status.HTTP_200_OK
    assert response4.json()['Date']==data['Date']
    assert response4.json()['Type']==data['Type']

#test deleting shift
def test_delete():
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    data = {'belongsTo': response1.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Evening"}
    response2 = client.post("/shift/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    response = client.delete("/shift/delete/"+response2.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    #try to delete again, expects 404
    response = client.delete("/shift/delete/"+response2.json()['_id'])
    assert response.status_code == status.HTTP_404_NOT_FOUND
