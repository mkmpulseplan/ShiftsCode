import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI,status
from fastapi.testclient import TestClient
from main import app
from  DAL.Constraints import * 
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

# test adding constraints
def test_add():
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    contents = [["Can","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    Date = (date.today()).isoformat()
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response2 = client.post("/constraints/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    assert response2.json()['belongsTo']==response1.json()['_id']
    for i in range(len(response2.json()['Contents'])):
        for n in range (len(response2.json()['Contents'][i])):
            assert response2.json()['Contents'][i][n]== contents[i][n]
    assert response2.json()['startsIn']==Date
    #try to add constraints with the same date and employee, should delete the first one and create the new one.
    random.shuffle(contents)
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response3 = client.post("/constraints/add", json=data)
    assert response3.status_code == status.HTTP_200_OK
    #make sure the new constraints are in place
    b = False
    for i in range(len(response3.json()['Contents'])):
        for n in range (len(response3.json()['Contents'][i])):
            if response2.json()['Contents'][i][n]!= response3.json()['Contents'][i][n]:
                b = True
    assert b == True 
    assert response3.json()['startsIn']==Date
    #try to create constraints with not 7 days, expect 400
    contents = [["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response = client.post("/constraints/add", json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    contents = [["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"],["Prefers Not","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"]]
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response = client.post("/constraints/add", json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    #try to create constraints with too much or too little per day, expects 400
    contents = [["Prefers Not"],["Can","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Prefers"],["Cannot","Prefers","Can"],["Prefers Not","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"]]
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response = client.post("/constraints/add", json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    contents = [["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not","Can"],["Can","Prefers","Prefers","Prefers Not"],["Cannot","Prefers","Can"],["Prefers Not","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"]]
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response = client.post("/constraints/add", json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    #delete the employee and try to create constraints, expects 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    contents = [["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response = client.post("/constraints/add", json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


#test find all constraints objects
def test_findAll():
    #create employee
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    #create constraints
    contents = [["Can","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    Date = (date.today()).isoformat()
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response2 = client.post("/constraints/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    Date2 = (date.today()+timedelta(days=1)).isoformat()
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date2}
    response3 = client.post("/constraints/add", json=data)
    assert response3.status_code == status.HTTP_200_OK
    #create employee
    data = create_employee()
    response4 = client.post("/employee/add", json = data)
    assert response4.status_code == status.HTTP_200_OK
    #create constraints
    contents = [["Can","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    Date = (date.today()).isoformat()
    data = {'belongsTo':response4.json()['_id'],'Contents': contents, 'startsIn': Date}
    response5 = client.post("/constraints/add", json=data)
    assert response5.status_code == status.HTTP_200_OK
    #check count of all constraints
    response = client.get("/constraints/all")
    assert response.status_code == status.HTTP_200_OK
    count = len(response.json())
    #delete a constraint object, expects lower count
    response = client.delete("/constraints/delete/"+response5.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/constraints/all")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json())==count-1


#test find all constraints with the same start date
def test_findByDate():
    #create employee
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    #create constraints
    contents = [["Can","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    Date = (date.today()).isoformat()
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response2 = client.post("/constraints/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    Date2 = (date.today()+timedelta(days=1)).isoformat()
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date2}
    response3 = client.post("/constraints/add", json=data)
    assert response3.status_code == status.HTTP_200_OK
    #create employee
    data = create_employee()
    response4 = client.post("/employee/add", json = data)
    assert response4.status_code == status.HTTP_200_OK
    #create constraints
    contents = [["Can","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    Date = (date.today()).isoformat()
    data = {'belongsTo':response4.json()['_id'],'Contents': contents, 'startsIn': Date}
    response5 = client.post("/constraints/add", json=data)
    assert response5.status_code == status.HTTP_200_OK
    response = client.get("/constraints/all_by_date/"+Date)
    for C in response.json():
        assert C['startsIn'] == Date


#test find all constraints with the same employee
def test_findByEmployee():
    #create employee
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    #create constraints
    contents = [["Can","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    Date = (date.today()).isoformat()
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response2 = client.post("/constraints/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    Date2 = (date.today()+timedelta(days=1)).isoformat()
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date2}
    response3 = client.post("/constraints/add", json=data)
    assert response3.status_code == status.HTTP_200_OK
    #create employee
    data = create_employee()
    response4 = client.post("/employee/add", json = data)
    assert response4.status_code == status.HTTP_200_OK
    #create constraints
    contents = [["Can","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    data = {'belongsTo':response4.json()['_id'],'Contents': contents, 'startsIn': Date}
    response5 = client.post("/constraints/add", json=data)
    assert response5.status_code == status.HTTP_200_OK
    response = client.get("/constraints/all_by_employee/"+response1.json()['_id'])
    for C in response.json():
        assert C['belongsTo'] == response1.json()['_id']

#test find all constraints with the same employee and start date
def test_findByEmployeeAndDate():
    #create employee
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    #create constraints
    contents = [["Can","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    Date = (date.today()).isoformat()
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response2 = client.post("/constraints/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    Date2 = (date.today()+timedelta(days=1)).isoformat()
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date2}
    response3 = client.post("/constraints/add", json=data)
    assert response3.status_code == status.HTTP_200_OK
    #create employee
    data = create_employee()
    response4 = client.post("/employee/add", json = data)
    assert response4.status_code == status.HTTP_200_OK
    #create constraints
    contents = [["Can","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    data = {'belongsTo':response4.json()['_id'],'Contents': contents, 'startsIn': Date}
    response5 = client.post("/constraints/add", json=data)
    assert response5.status_code == status.HTTP_200_OK
    data = {'belongsTo': response4.json()['_id'],'startsIn': Date}
    response = client.post("/constraints/all_by_employee_and_date", json=data)
    assert response.json()['belongsTo'] == response4.json()['_id'] and response.json()['startsIn']==Date


#test editing a constraint
def test_edit():
    #create employee
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    #create constraints
    contents = [["Can","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    Date = (date.today()).isoformat()
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response2 = client.post("/constraints/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    contents = [["Prefers","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"],["Cannot","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Unavailable","Prefers"],["Cannot","Prefers","Can"]]
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response = client.put("/constraints/edit", json=data)
    assert response.status_code == status.HTTP_200_OK
    for i in range(len(response.json()['Contents'])):
        for n in range (len(response.json()['Contents'][i])):
            assert response.json()['Contents'][i][n]== contents[i][n]
    #delete the employee and try again, expects 404
    response = client.delete("/employee/delete/"+response1.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    response = client.put("/constraints/edit", json=data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

#test deleting a constraint
def test_delete():
    #create employee
    data = create_employee()
    response1 = client.post("/employee/add", json = data)
    assert response1.status_code == status.HTTP_200_OK
    #create constraints
    contents = [["Can","Cannot","Prefers Not"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Can","Can"],["Prefers Not","Cannot","Prefers Not"],["Can","Prefers","Prefers"],["Cannot","Prefers","Can"]]
    Date = (date.today()).isoformat()
    data = {'belongsTo':response1.json()['_id'],'Contents': contents, 'startsIn': Date}
    response2 = client.post("/constraints/add", json=data)
    assert response2.status_code == status.HTTP_200_OK
    response = client.delete("/constraints/delete/"+response2.json()['_id'])
    assert response.status_code == status.HTTP_200_OK
    #try to delete again, expects 404
    response = client.delete("/constraints/delete/"+response2.json()['_id'])
    assert response.status_code == status.HTTP_404_NOT_FOUND


