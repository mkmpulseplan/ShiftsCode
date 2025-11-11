from fastapi import APIRouter,Response,status
from DAL.SwitchRequest import *
from API.Shift import api_switch
from DAL.Shift import *
from DAL.Employee import *
from datetime import date
router = APIRouter(prefix="/Switch")

# find all switch requests
@router.get("/all")
def api_get_all():
    return SwitchRequest.find().run()

#add new
@router.post("/add")
def api_add(request:SwitchRequest):
    employee:Employee = Employee.get(request.From).run()
    employee2:Employee = Employee.get(request.to).run()
    if employee == None or employee2 == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        new_request:SwitchRequest = SwitchRequest(From=request.From, to=request.to, FromShiftID=request.FromShiftID, ToShiftID=request.ToShiftID, ManagerStatus = "N/A", EmployeeStatus="Pending")
        new_request.save()
        return new_request

# employee status change
@router.put("/employee_change_status")
def api_employee_change_status(request:SwitchRequest):
    the_request:SwitchRequest = SwitchRequest.get(request.id).run()
    if the_request == None:
        print("switch request not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        the_request.EmployeeStatus = request.EmployeeStatus
        if the_request.EmployeeStatus == "Approved":
            the_request.ManagerStatus = "Pending"
        else:
            the_request.ManagerStatus = "N/A"
        the_request.save()
        return the_request

# manager status change
@router.put("/manager_change_status")
def api_manager_change_status(request:SwitchRequest):
    the_request:SwitchRequest = SwitchRequest.get(request.id).run()
    if the_request == None:
        print("switch request not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        the_request.ManagerStatus = request.ManagerStatus
        if the_request.ManagerStatus == "Approved":

            switch:Switches = Switches(shift1=the_request.FromShiftID, shift2=the_request.ToShiftID)
            api_switch(switch)
        the_request.save()
        return the_request

#delete
@router.delete("/delete/{SRid}")
def api_delete(SRid:str):
    the_request:SwitchRequest = SwitchRequest.get(SRid).run()
    if the_request == None:
        print("switch request not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        the_request.delete()
        return Response(status_code=status.HTTP_200_OK)
    

    