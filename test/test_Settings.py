import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI,status
from fastapi.testclient import TestClient
from main import app
from pydantic import TypeAdapter

client = TestClient(app)


#test editing the settings
def test_edit():
    data = {'id':"This does not matter:)", 'TwelveHourShifts': True, 'MinimumShifts': 4, 'ShmoneShmone':True, 'Max2ShiftsSameType': False}
    response = client.put("/settings/edit", json=data)
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/settings/find")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id']=="Settings@ABC!!2016#"
    assert response.json()['TwelveHourShifts']== data['TwelveHourShifts']
    assert response.json()['MinimumShifts']== data['MinimumShifts']
    assert response.json()['ShmoneShmone']== data['ShmoneShmone']
    assert response.json()['Max2ShiftsSameType']== data['Max2ShiftsSameType']

#test resetting the settings
def test_reset():
    response = client.put("/settings/reset")
    assert response.status_code == status.HTTP_200_OK
    response = client.get("/settings/find")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['_id']=="Settings@ABC!!2016#"
    assert response.json()['TwelveHourShifts']== False
    assert response.json()['MinimumShifts']== 2
    assert response.json()['ShmoneShmone']== True
    assert response.json()['Max2ShiftsSameType']== True