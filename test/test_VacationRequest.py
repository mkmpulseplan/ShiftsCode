import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI,status
from fastapi.testclient import TestClient
from main import app
from pydantic import TypeAdapter
import random 
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

#test adding a new vacation request
def test_add():
    data = create_employee()
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_200_OK
    InaWeek = date.today()+timedelta(days=7)
    data = {'belongsTo': response.json()['_id'],'startsIn':(date.today()).isoformat(), 'endsIn': InaWeek.isoformat(), 'Status': " "}
    response1 = client.post("/Vacation/add", json=data)
    assert response1.status_code == status.HTTP_200_OK
    assert response1.json()['belongsTo']==data['belongsTo']
    assert response1.json()['startsIn']==data['startsIn']
    assert response1.json()['endsIn']==data['endsIn']
    assert response1.json()['Status']=='Pending'
    #delete the employee and try to create a vacation request, should get 404
    response = client.delete("/employee/delete/"+response1.json()['belongsTo'])
    assert response.status_code == status.HTTP_200_OK 
    response = client.post("/Vacation/add", json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

#test changing the request status
def test_changeStatus():
    data = create_employee()
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_200_OK
    InaWeek = date.today()+timedelta(days=7)
    data = {'belongsTo': response.json()['_id'],'startsIn':(date.today()).isoformat(), 'endsIn': InaWeek.isoformat(), 'Status': " "}
    response1 = client.post("/Vacation/add", json=data)
    assert response1.status_code == status.HTTP_200_OK
    assert response1.json()['Status']=='Pending'
    data = {'belongsTo': response.json()['_id'],'startsIn':(date.today()).isoformat(), 'endsIn': InaWeek.isoformat(), 'Status': "Approved"}
    response1 = client.post("/Vacation/change_status", json=data)
    assert response1.status_code == status.HTTP_200_OK
    assert response1.json()['Status']==data['Status']

#test deleting a vacation request
def test_delete():
    data = create_employee()
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_200_OK
    InaWeek = date.today()+timedelta(days=7)
    data = {'belongsTo': response.json()['_id'],'startsIn':(date.today()).isoformat(), 'endsIn': InaWeek.isoformat(), 'Status': " "}
    response1 = client.post("/Vacation/add", json=data)
    assert response1.status_code == status.HTTP_200_OK
    response = client.delete("/Vacation/delete"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    #try to delete again, expects 404
    response = client.delete("/Vacation/delete"+response1.json()['_id'])
    assert response.status_code == status.HTTP_404_NOT_FOUND
