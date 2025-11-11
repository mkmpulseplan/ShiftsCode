import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI,status
from fastapi.testclient import TestClient
from main import app
from  DAL.Employee import * 
import random
from pydantic import TypeAdapter

client = TestClient(app)

#create a data object for employee creation
def create_employee():
    random_int = random.randint(0,100000000000)
    id = "test_"+str(random_int)
    lastName = "XxX"
    password = "test123"
    data = {'id': id, "lastName": lastName, "password": password}
    return data

#test adding a support query
def test_add():
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    print(response1.json()['_id'])
    assert response1.status_code == status.HTTP_200_OK
    data = {'From': response1.json()['_id'], 'Subject': "Test", 'Contents':"Test Test Testing a Test", 'isPending':True}
    response = client.post("/support/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['From']==data['From']
    assert response.json()['Subject']==data['Subject']
    assert response.json()['Contents']==data['Contents']
    assert response.json()['isPending']==True
    #delete the employee and attempt to add another support, expect 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.post("/support/add", json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

#test toggling the isPending status
def test_toggleIsPending():
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    data = {'From': response1.json()['_id'], 'Subject': "Test", 'Contents':"Test Test Testing a Test", 'isPending':True}
    response2 = client.post("/support/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json()['isPending']==True
    response = client.put("/support/toggle_pending/"+response2.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['isPending']==False
    response = client.put("/support/toggle_pending/"+response2.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['isPending']==True
    #delete the support query and try to toggle, should return 404
    response = client.delete("/support/delete/"+response2.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.put("/support/toggle_pending/"+response2.json()['_id'])
    assert response.status_code == status.HTTP_404_NOT_FOUND

#test deleting a support query
def test_delete():
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    data = {'From': response1.json()['_id'], 'Subject': "Test", 'Contents':"Test Test Testing a Test", 'isPending':True}
    response2 = client.post("/support/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    response = client.delete("/support/delete/"+response2.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    #try to delete again, should get 404
    response = client.delete("/support/delete/"+response2.json()['_id'])
    assert response.status_code == status.HTTP_404_NOT_FOUND