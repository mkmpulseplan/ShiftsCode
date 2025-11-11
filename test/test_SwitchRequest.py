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


def test_add():
    #create employees and shifts to switch 
    data = create_employee()
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Evening"}
    response1 = client.post("/shift/add", json=data)
    assert response1.status_code == status.HTTP_200_OK
    data = create_employee()
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Morning"}
    response2 = client.post("/shift/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    #create a switch request
    data = {'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"",'EmployeeStatus':""}
    response = client.post("/Switch/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['From']==data['From']
    assert response.json()['to']==data['to']
    assert response.json()['FromShift']==data['FromShift']
    assert response.json()['ToShift']==data['ToShift']
    assert response.json()['ManagerStatus']=='N/A'
    assert response.json()['EmployeeStatus']=='Pending'

#test employee change status
def test_employeeChangeStatus():
    #create employees and shifts to switch 
    data = create_employee()
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Evening"}
    response1 = client.post("/shift/add", json=data)
    assert response1.status_code == status.HTTP_200_OK
    data = create_employee()
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Morning"}
    response2 = client.post("/shift/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    #create a switch request
    data = {'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"",'EmployeeStatus':""}
    response = client.post("/Switch/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    #change status- approved
    data = {'id': response.json()['_id'],'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"",'EmployeeStatus':"Approved"}
    response= client.put("/Switch/employee_change_status", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['EmployeeStatus']=="Approved"
    assert response.json()['ManagerStatus']=="Pending"
    #change status- denied
    data = {'id': response.json()['_id'],'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"",'EmployeeStatus':"Denied"}
    response= client.put("/Switch/employee_change_status", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['EmployeeStatus']=="Denied"
    assert response.json()['ManagerStatus']=="N/A"
    #delete the request and try to change the status again, expects 404
    response3 = client.delete("/Switch/delete/"+response.json()['_id'])
    assert response3.status_code == status.HTTP_200_OK
    data = {'_id': response.json()['_id'],'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"",'EmployeeStatus':"Denied"}
    response= client.put("/Switch/employee_change_status", json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

#test manager change status
def test_managerChangeStatus():
    #create employees and shifts to switch 
    data = create_employee()
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Evening"}
    response1 = client.post("/shift/add", json=data)
    assert response1.status_code == status.HTTP_200_OK
    data = create_employee()
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Morning"}
    response2 = client.post("/shift/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    #create a switch request
    data = {'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"",'EmployeeStatus':""}
    response = client.post("/Switch/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    #change status- approved
    data = {'id': response.json()['_id'],'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"Approved",'EmployeeStatus':"Approved"}
    response= client.put("/Switch/manager_change_status", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['ManagerStatus']=="Approved"
    #make sure the switch happened
    data = {'Date':response1.json()['Date'],'Type':response1.json()['Type']}
    response = client.post("/shift/by_date_and_type", json=data)
    assert response.json()['belongsTo']==response2.json()['belongsTo']
    data = {'Date':response2.json()['Date'],'Type':response2.json()['Type']}
    response = client.post("/shift/by_date_and_type", json=data)
    assert response.json()['belongsTo']==response1.json()['belongsTo']
    #create a switch request
    data = {'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"",'EmployeeStatus':""}
    response = client.post("/Switch/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    #change status- denied
    data = {'id': response.json()['_id'],'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"Denied",'EmployeeStatus':"Denied"}
    response= client.put("/Switch/manager_change_status", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['ManagerStatus']=="Denied"
    #delete the request and try to change the status again, expects 404
    response3 = client.delete("/Switch/delete/"+response.json()['_id'])
    assert response3.status_code == status.HTTP_200_OK
    data = {'id': response.json()['_id'],'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"Denied",'EmployeeStatus':"Denied"}
    response= client.put("/Switch/manager_change_status", json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

#test deleting a request
def test_delete():
    #create employees and shifts to switch 
    data = create_employee()
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Evening"}
    response1 = client.post("/shift/add", json=data)
    assert response1.status_code == status.HTTP_200_OK
    data = create_employee()
    response = client.post("/employee/add", json = data)
    assert response.status_code == status.HTTP_200_OK
    data = {'belongsTo': response.json()['_id'], 'Date':(date.today()).isoformat(), 'Day':(date.today()).strftime("%A"), 'Type': "Morning"}
    response2 = client.post("/shift/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    #create a switch request
    data = {'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"",'EmployeeStatus':""}
    response = client.post("/Switch/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    #change status- approved
    data = {'id': response.json()['_id'],'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"Approved",'EmployeeStatus':"Approved"}
    response= client.put("/Switch/manager_change_status", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['ManagerStatus']=="Approved"
    #make sure the switch happened
    data = {'Date':response1.json()['Date'],'Type':response1.json()['Type']}
    response = client.post("/shift/by_date_and_type", json=data)
    assert response.json()['belongsTo']==response2.json()['belongsTo']
    data = {'Date':response2.json()['Date'],'Type':response2.json()['Type']}
    response = client.post("/shift/by_date_and_type", json=data)
    assert response.json()['belongsTo']==response1.json()['belongsTo']
    #create a switch request
    data = {'From': response1.json()['belongsTo'], 'to': response2.json()['belongsTo'], 'FromShiftID': response1.json()['_id'], "ToShiftID":response2.json()['_id'],'ManagerStatus':"",'EmployeeStatus':""}
    response = client.post("/Switch/add", json=data)
    assert response.status_code == status.HTTP_200_OK
    response = client.delete("/Switch/delete/"+response.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    #try to delete again, expects 404
    response = client.delete("/Switch/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_404_NOT_FOUND
