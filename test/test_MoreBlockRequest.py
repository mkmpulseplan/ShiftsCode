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

#test adding a more block request
def test_add():
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    response = client.post("/moreBlockRequest/add/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id']==response1.json()['_id']
    InaWeek = date.today()+timedelta(days=7)
    assert response.json()['ExpiresIn']==InaWeek
    assert response.json()['Status']=="Pending"
    #delete the user and try to create a request, expects 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/moreBlockRequest/add/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_404_NOT_FOUND

#test finding all requests
def test_findAll():
    #create requests
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    response = client.post("/moreBlockRequest/add/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    response = client.post("/moreBlockRequest/add/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    response = client.post("/moreBlockRequest/add/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/moreBlockRequest/all")
    assert response.status_code == status.HTTP_200_OK
    count = len(response.json())
    #delete a request and make sure the count is down
    response = client.delete("/moreBlockRequest/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/moreBlockRequest/all")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json())==count-1

#test changing a request's status
def test_edit():
    #create request
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    response = client.post("/moreBlockRequest/add/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    data = {'id': response1.json()['_id'], 'new_status': "Approved"}
    response = client.put("/moreBlockRequest/changeStatus", json = data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['Status']=="Approved"
    #delete the employee and try to edit again, expects 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.put("/moreBlockRequest/changeStatus", json = data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

#test deleting a request
def test_delete():
    #create request
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    response = client.post("/moreBlockRequest/add/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.delete("/moreBlockRequest/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    #try to delete again, expects 404
    response = client.delete("/moreBlockRequest/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_404_NOT_FOUND


