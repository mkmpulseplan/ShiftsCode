from fastapi import APIRouter,Response,status
from DAL.SupportQuery import *
from DAL.Employee import *

router = APIRouter(prefix="/support")

# find all supportQueries
@router.get("/all")
def api_get_all():
    return SupportQuery.find().run()

# find all pending supportQueries
@router.get("/all_pending")
def api_get_all_pending():
    result = SupportQuery.find().run()
    Filtered = []
    for SQ in result:
        if SQ.isPending==True:
            Filtered.append(SQ)
    return Filtered

# find all supportQueries by employee
@router.get("/by_employee/{Employee_Name}")
def api_get_by_employee(Employee_Name):
    result = SupportQuery.find().run()
    Filtered = []
    for SQ in result:
        if SQ.From==Employee_Name:
            Filtered.append(SQ)
    return Filtered

# add a support query
@router.post("/add")
def api_add(support:SupportQuery):
    print(support.From)
    employee:Employee = Employee.get(support.From).run()
    if employee == None:
        print("employee not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        new_support:SupportQuery = SupportQuery(From=support.From, Subject=support.Subject, Contents=support.Contents, isPending=True)
        new_support.save()
        return new_support
    
# toggle pending status
@router.put("/toggle_pending/{Support_id}")
def api_toggle_pending(Support_id):
    support:SupportQuery = SupportQuery.get(Support_id).run()
    if support == None:
        print("support query not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        employee:Employee = Employee.get(support.From).run()
        if employee == None:
            print("employee not found")
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        else:
            if support.isPending== True:
                support.isPending = False
            else: 
                support.isPending = True
            support.save()
            return support


# delete a support query
@router.delete("/delete/{Support_id}")
def api_delete(Support_id):
    support:SupportQuery = SupportQuery.get(Support_id).run()
    if support == None:
        print("support query not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        support.delete()
        return Response(status_code=status.HTTP_200_OK)