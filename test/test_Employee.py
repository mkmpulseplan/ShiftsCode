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

# test adding an employee
def test_add():
    data = create_employee()
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id'] == data['id']
    assert response.json()['lastName'] == data['lastName']
    assert response.json()['password'] == data['password']
    assert response.json()['isApproved'] == False
    assert response.json()['isHidden'] == True
    assert response.json()['isManager'] == False
    assert response.json()['isDev'] == False
    assert response.json()['isLastResort'] == False
    assert response.json()['isNationalService'] == False
    assert response.json()['NeverBreak88'] == False
    #try to add the same employee again, expect a 400 error
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    #delete the user
    response = client.delete("/employee/delete/"+data['id'])
    assert response.status_code == status.HTTP_200_OK

#test finding all employees
def test_findAll():
    data1 = create_employee()
    response = client.post("/employee/add", json = data1)
    assert response.status_code == status.HTTP_200_OK
    data2 = create_employee()
    response = client.post("/employee/add", json = data2)
    assert response.status_code == status.HTTP_200_OK
    data3 = create_employee()
    response = client.post("/employee/add", json = data3)
    assert response.status_code == status.HTTP_200_OK
    data4 = create_employee()
    response = client.post("/employee/add", json = data4)
    assert response.status_code == status.HTTP_200_OK

    response = client.get("/employee/all")
    assert response.status_code == status.HTTP_200_OK
    count = len(response.json())

    #remove an employee, make sure the count is down
    response = client.delete("/employee/delete/"+data4['id'])
    assert response.status_code == status.HTTP_200_OK
    
    response = client.get("/employee/all")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == count-1

    #add an employee, make sure the count is up
    data4 = create_employee()
    response = client.post("/employee/add", json = data4)
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/employee/all")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == count

    #delete the employees
    response = client.delete("/employee/delete/"+data1['id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.delete("/employee/delete/"+data2['id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.delete("/employee/delete/"+data3['id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.delete("/employee/delete/"+data4['id'])


#test finding all non hidden employees    
def test_findAllNonHidden():
    #create employees
    data1 = create_employee()
    response = client.post("/employee/add", json = data1)
    assert response.status_code == status.HTTP_200_OK
    data2 = create_employee()
    response = client.post("/employee/add", json = data2)
    assert response.status_code == status.HTTP_200_OK
    data3 = create_employee()
    response = client.post("/employee/add", json = data3)
    assert response.status_code == status.HTTP_200_OK
    data4 = create_employee()
    response = client.post("/employee/add", json = data4)
    assert response.status_code == status.HTTP_200_OK

    #toggle some statuses
    response = client.put("/employee/toggle_hidden/"+data3['id'])
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['isHidden'] == False
    response = client.put("/employee/toggle_hidden/"+data2['id'])
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['isHidden'] == False

    #try to find all non hidden employees
    response = client.get("/employee/all_non_hidden")
    assert response.status_code == status.HTTP_200_OK
    for E in response.json():
        assert E['isHidden']==False

    #delete the employees
    response = client.delete("/employee/delete/"+data1['id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.delete("/employee/delete/"+data2['id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.delete("/employee/delete/"+data3['id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.delete("/employee/delete/"+data4['id'])

#test find by name
def test_findByName():
    data1 = create_employee()
    response1 = client.post("/employee/add", json = data1)
    assert response1.status_code == status.HTTP_200_OK
    response2 = client.get("/employee/"+response1.json()['_id'])
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json()['_id'] == response1.json()['_id']
    assert response2.json()['lastName'] == response1.json()['lastName']
    assert response2.json()['password'] == response1.json()['password']
    assert response2.json()['isApproved'] == response1.json()['isApproved']
    assert response2.json()['isHidden'] == response1.json()['isHidden']
    assert response2.json()['isManager'] == response1.json()['isManager']
    assert response2.json()['isDev'] == response1.json()['isDev']
    assert response2.json()['isLastResort'] == response1.json()['isLastResort']
    assert response2.json()['isNationalService'] == response1.json()['isNationalService']
    assert response2.json()['NeverBreak88'] == response1.json()['NeverBreak88']
    #delete the user and try to find it, expects none
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response2 = client.get("/employee/"+response1.json()['_id'])
    assert response2.json()==None

#test toggling manager status
def test_toggleManagerStatus():
    data1 = create_employee()
    response1 = client.post("/employee/add", json = data1)
    assert response1.status_code == status.HTTP_200_OK
    response2 = client.put("/employee/toggle_manager/"+response1.json()['_id'])
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json()['isManager']!=response1.json()['isManager']
    #delete the user and try to toggle again, expects 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response2 = client.put("/employee/toggle_manager/"+response1.json()['_id'])
    assert response2.status_code == status.HTTP_404_NOT_FOUND

#test toggling hidden status
def test_toggleHiddenStatus():
    data1 = create_employee()
    response1 = client.post("/employee/add", json = data1)
    assert response1.status_code == status.HTTP_200_OK
    response2 = client.put("/employee/toggle_hidden/"+response1.json()['_id'])
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json()['isHidden']!=response1.json()['isHidden']
    #delete the user and try to toggle again, expects 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response2 = client.put("/employee/toggle_hidden/"+response1.json()['_id'])
    assert response2.status_code == status.HTTP_404_NOT_FOUND

#test toggling last resort status
def test_toggleLastResortStatus():
    data1 = create_employee()
    response1 = client.post("/employee/add", json = data1)
    assert response1.status_code == status.HTTP_200_OK
    response2 = client.put("/employee/toggle_last_resort/"+response1.json()['_id'])
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json()['isLastResort']!=response1.json()['isLastResort']
    #delete the user and try to toggle again, expects 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response2 = client.put("/employee/toggle_last_resort/"+response1.json()['_id'])
    assert response2.status_code == status.HTTP_404_NOT_FOUND

#test toggling National Service status
def test_toggleNationalServiceStatus():
    data1 = create_employee()
    response1 = client.post("/employee/add", json = data1)
    assert response1.status_code == status.HTTP_200_OK
    response2 = client.put("/employee/toggle_national_service/"+response1.json()['_id'])
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json()['isNationalService']!=response1.json()['isNationalService']
    #delete the user and try to toggle again, expects 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response2 = client.put("/employee/toggle_national_service/"+response1.json()['_id'])
    assert response2.status_code == status.HTTP_404_NOT_FOUND

#test toggling Never break 8-8 rule status
def test_toggleNeverBreak88Status():
    data1 = create_employee()
    response1 = client.post("/employee/add", json = data1)
    assert response1.status_code == status.HTTP_200_OK
    response2 = client.put("/employee/toggle_88_rule/"+response1.json()['_id'])
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json()['NeverBreak88']!=response1.json()['NeverBreak88']
    #delete the user and try to toggle again, expects 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response2 = client.put("/employee/toggle_88_rule/"+response1.json()['_id'])
    assert response2.status_code == status.HTTP_404_NOT_FOUND

#test approving an employee
def test_approve():
    data1 = create_employee()
    response1 = client.post("/employee/add", json = data1)
    assert response1.status_code == status.HTTP_200_OK
    response = client.put("/employee/approve/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['isApproved']==True
    assert response.json()['isHidden']==False
    #delete the user and try to approve again, expects 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response2 = client.put("/employee/approve/"+response1.json()['_id'])
    assert response2.status_code == status.HTTP_404_NOT_FOUND

#test deleting an employee
def test_delete():
    data1 = create_employee()
    response1 = client.post("/employee/add", json = data1)
    assert response1.status_code == status.HTTP_200_OK
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    #try to delete again. expects 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_404_NOT_FOUND

#test login
def test_login():
    data1 = create_employee()
    response1 = client.post("/employee/add", json = data1)
    assert response1.status_code == status.HTTP_200_OK
    data2 = {'id': response1.json()['_id'], 'password': response1.json()['password']}
    response2 = client.post("/employee/Login", json=data2)
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json()['_id']==response1.json()['_id']
    #test with wrong password, expects 404
    data2 = {'id': response1.json()['_id'], 'password': response1.json()['password']+"123"}
    response2 = client.post("/employee/Login", json=data2)
    assert response2.status_code == status.HTTP_404_NOT_FOUND
    #delete the user and try to login, expects 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    data2 = {'id': response1.json()['_id'], 'password': response1.json()['password']}
    response2 = client.post("/employee/Login", json=data2)
    assert response2.status_code == status.HTTP_404_NOT_FOUND
