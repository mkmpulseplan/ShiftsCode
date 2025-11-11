from fastapi import APIRouter,Response,status
from DAL.Shift import *
from DAL.Employee import *

router = APIRouter(prefix="/shift")

#find all shifts
@router.get("/all")
def api_get_all():
    return Shift.find().run()

#find by employee
@router.get("/all_by_employee/{Employee_Name}")
def api_get_by_employee(Employee_Name):
    employee:Employee = Employee.get(Employee_Name).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    result = Shift.find().run()
    Filtered = []
    for S in result:
        if S.belongsTo==Employee_Name:
            Filtered.append(S)
    return Filtered

#find by date
@router.get("/all_by_date/{Date}")
def api_get_by_date(Date: date):
    result = Shift.find().run()
    Filtered = []
    for S in result:
        if S.Date==Date:
            Filtered.append(S)
    return Filtered

#find by date and type
@router.post("/by_date_and_type")
def api_get_by_date_and_type(filter:Filter):
    result = Shift.find().run()
    for S in result:
        if S.Date==filter.Date and S.Type==filter.Type:
            return S

#create a shift
@router.post("/add")
def api_add_a_shift(shift: Shift):
    new_shift:Shift = Shift(belongsTo=shift.belongsTo, Date=shift.Date, Day=shift.Day, Type=shift.Type)
    result = Shift.find().run()
    for s in result:
        if s.Date == shift.Date and s.Type == shift.Type:
            s.delete()
    new_shift.save()
    return new_shift

 
#switch
@router.put("/Switch")
def api_switch(switch:Switches):
    new_shift1 = Shift.get(switch.shift1).run()
    new_shift2 = Shift.get(switch.shift2).run()
    owner1:Employee = Employee.get(new_shift1.belongsTo).run()
    owner2:Employee = Employee.get(new_shift2.belongsTo).run()
    if owner1 == None or owner2 == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if new_shift1 == None or new_shift2 == None:
            print("shift not found")
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        else: 
            new_shift1.belongsTo =owner2.id
            new_shift2.belongsTo=owner1.id
            new_shift1.save()
            new_shift2.save()

#delete a shift
@router.delete("/delete/{Sid}")
def api_delete(Sid):
    shift:Shift = Shift.get(Sid).run()
    if shift == None:
        print("shift not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        shift.delete()
        return Response(status_code=status.HTTP_200_OK)      