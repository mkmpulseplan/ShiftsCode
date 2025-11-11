from fastapi import APIRouter,Response,status
from DAL.MoreBlockRequest import *
from DAL.Employee import *
from datetime import date, timedelta
router = APIRouter(prefix="/moreBlockRequest")

# find all more block requests
@router.get("/all")
def api_get_all():
    return MoreBlockRequest.find().run()

# find by name 
@router.get("/by_employee/{Employee_Name}")
def api_find_by_employee(Employee_Name):
    return MoreBlockRequest.get(Employee_Name).run()

# add a more block request
@router.post("/add/{Employee_Name}")
def api_add(Employee_Name):
    employee:Employee = Employee.get(Employee_Name).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        request:MoreBlockRequest = MoreBlockRequest.get(Employee_Name).run()
        if request!=None:
            request.delete()     
        InaWeek = date.today()+timedelta(days=7)
        new_request:MoreBlockRequest = MoreBlockRequest(id=Employee_Name, ExpiresIn=InaWeek, Status="Pending")
        new_request.save()
        return new_request
        
# change a more block request's status
@router.put("/changeStatus")
def api_change_status(CS: ChangeStatus):
    employee: Employee = Employee.get(CS.id).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        request:MoreBlockRequest = MoreBlockRequest.get(CS.id).run()
        if request==None:
            print("request not found")
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        else:
            edited_request: MoreBlockRequest = MoreBlockRequest(id=request.id, ExpiresIn=request.ExpiresIn, Status=CS.new_status)
            edited_request.save()
            return edited_request

# delete a more block request
@router.delete("/delete/{Employee_Name}")
def api_delete(Employee_Name):
    employee: Employee = Employee.get(Employee_Name).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        request: MoreBlockRequest = MoreBlockRequest.get(Employee_Name).run()
        if request==None:
            print("request not found")
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        else:
            request.delete()
            return Response(status_code=status.HTTP_200_OK)
            

