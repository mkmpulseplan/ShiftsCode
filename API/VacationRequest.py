from fastapi import APIRouter,Response,status
from DAL.VacationRequest import *
from DAL.Employee import *
from datetime import date
router = APIRouter(prefix="/Vacation")

# find all vacation requests
@router.get("/all")
def api_get_all():
    return VacationRequest.find().run()

#create a new vacation request
@router.post("/add")
def api_add(request: VacationRequest):
    employee:Employee = Employee.get(request.belongsTo).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        new_request:VacationRequest = VacationRequest(belongsTo=request.belongsTo, startsIn=request.startsIn, endsIn=request.endsIn, Status="Pending")
        new_request.save()
        return new_request

#change request's status
@router.put("/change_status")
def api_change_status(request: VacationRequest):
    the_request:VacationRequest = VacationRequest.find(request.id).run()
    if the_request == None:
        print("vacation request not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        the_request.Status = request.Status
        the_request.save()

#delete a vacation request
@router.delete("/delete/{Rid}")
def api_delete(Rid):
    the_request:VacationRequest = VacationRequest.get(Rid).run()
    if the_request == None:
        print("vacation request not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        the_request.delete()
        return Response(status_code=status.HTTP_200_OK) 