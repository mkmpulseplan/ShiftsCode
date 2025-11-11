from fastapi import APIRouter,Response,status
from DAL.Employee import *
import API.MoreBlockRequest as MoreBlockRequest
import API.SupportQuery as SupportQuery
import API.Constraints as Constraints
import API.SwitchRequest as SwitchRequest
import API.VacationRequest as VacationRequest

router = APIRouter(prefix="/employee")

# find all employees
@router.get("/all")
def api_get_all():
    return Employee.find().run()

# find all non-hidden employees
@router.get("/all_non_hidden")
def api_get_all_non_hidden():
    result = Employee.find().run()
    Filtered = []
    for E in result:
        if E.isHidden != True:
            Filtered.append(E)
    return Filtered

# find by name
@router.get("/{Employee_Name}")
def api_find_employee(Employee_Name):
    return Employee.get(Employee_Name).run()


# toggle Manager status
@router.put("/toggle_manager/{Employee_Name}")
def api_toggle_manager(Employee_Name):
    employee:Employee = Employee.get(Employee_Name).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if employee.isManager== True:
            employee.isManager = False
        else: 
            employee.isManager = True
        employee.save()
        return employee

# toggle Hidden status
@router.put("/toggle_hidden/{Employee_Name}")
def api_toggle_hidden(Employee_Name):
    employee:Employee = Employee.get(Employee_Name).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if employee.isHidden== True:
            employee.isHidden = False
        else: 
            employee.isHidden = True
        employee.save()
        return employee

# toggle Last Resort status
@router.put("/toggle_last_resort/{Employee_Name}")
def api_toggle_last_resort(Employee_Name):
    employee:Employee = Employee.get(Employee_Name).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if employee.isLastResort== True:
            employee.isLastResort = False
        else: 
            employee.isLastResort = True
        employee.save()
        return employee

# toggle National Service status
@router.put("/toggle_national_service/{Employee_Name}")
def api_toggle_national_service(Employee_Name):
    employee:Employee = Employee.get(Employee_Name).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if employee.isNationalService== True:
            employee.isNationalService = False
        else: 
            employee.isNationalService = True
        employee.save()
        return employee

# toggle never break 8-8 status
@router.put("/toggle_88_rule/{Employee_Name}")
def api_toggle_88_rule(Employee_Name):
    employee:Employee = Employee.get(Employee_Name).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if employee.NeverBreak88== True:
            employee.NeverBreak88 = False
        else: 
            employee.NeverBreak88 = True
        employee.save()
        return employee

# approve an employee
@router.put("/approve/{Employee_Name}")
def api_approve(Employee_Name):
    employee:Employee = Employee.get(Employee_Name).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        employee.isApproved = True
        employee.isHidden = False
        employee.save()
        return employee
    
# add an employee
@router.post("/add")
def api_add(employee:New):
    the_employee:Employee = Employee.get(employee.id).run()
    if the_employee != None:
        print("this employee already exists")
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        new_employee:Employee = Employee(id=employee.id, lastName=employee.lastName, password=employee.password, isApproved=False, isHidden=True,isManager=False,isDev=False,isLastResort=False,isNationalService=False,NeverBreak88=False)
        new_employee.save()
        return new_employee

# delete an employee
@router.delete("/delete/{Employee_Name}")
def api_delete(Employee_Name):
    employee:Employee = Employee.get(Employee_Name).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        MBR = MoreBlockRequest.api_find_by_employee(Employee_Name)
        if MBR != None:
            MoreBlockRequest.api_delete(Employee_Name)
        supportLST = SupportQuery.api_get_by_employee(Employee_Name)
        for s in (supportLST):
            SupportQuery.api_delete(s.id)
        ConstraintsLST = Constraints.api_find_by_name(Employee_Name)
        for C in (ConstraintsLST):
            Constraints.api_delete(C.id)
        SwitchRequests = SwitchRequest.api_get_all()
        for SR in SwitchRequests:
            if SR.From == Employee_Name or SR.to == Employee_Name:
                SwitchRequest.api_delete(SR.id)
        VacationRequests = VacationRequest.api_get_all()
        for VR in VacationRequests:
            if VR.belongsTo == Employee_Name:
                VacationRequest.api_delete(VR.id)
        employee.delete()
        return Response(status_code=status.HTTP_200_OK)
    
# login
@router.post("/Login")
def api_Login(EL:Login):
    employee:Employee = Employee.get(EL.id).run()
    if employee == None:
        print("Login went wrong")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    elif employee.password != EL.password:
        print("Login went wrong")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return employee
    
    