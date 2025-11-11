from fastapi import APIRouter,Response,status
from DAL.Employee import *
from DAL.Constraints import *

router = APIRouter(prefix="/constraints")

# find all constraints
@router.get("/all")
def api_get_all():
    return Constraints.find().run()

# find by start date
@router.get("/all_by_date/{Date}")
def api_get_all_non_hidden(Date):
    result = Constraints.find().run()
    Filtered = []
    for C in result:
        if C.startsIn == Date:
            Filtered.append(C)
    return Filtered

# find by name
@router.get("/all_by_employee/{Employee_Name}")
def api_find_by_name(Employee_Name):
    result = Constraints.find().run()
    Filtered = []
    for C in result:
        if C.belongsTo == Employee_Name:
            Filtered.append(C)
    return Filtered

#find by name and start date
@router.post("/all_by_employee_and_date")
def api_find_by_name_and_date(filter:Filter):
    result = Constraints.find().run()
    for C in result:
        if C.startsIn == filter.startsIn and C.belongsTo==filter.belongsTo:
            return C
 
# add a constraints
@router.post("/add")
def api_add(constraints:Constraints):
    filter = Filter(belongsTo=constraints.belongsTo, startsIn=constraints.startsIn)
    the_constraints:Constraints = api_find_by_name_and_date(filter)
    if the_constraints != None:
        the_constraints.delete()
    employee:Employee = Employee.get(constraints.belongsTo).run()
    if employee == None:
        print("The employee was not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        
        if len(constraints.Contents)!=7:
            print("Constraints are not for exactly a week")
            return Response(status_code=status.HTTP_400_BAD_REQUEST)
        else:
            for i in range(len(constraints.Contents)):
                if len(constraints.Contents[i])<2 or len(constraints.Contents[i])>3:
                    print("Constraints structure is not right")
                    return Response(status_code=status.HTTP_400_BAD_REQUEST)
        new_constraints:Constraints = Constraints(belongsTo=constraints.belongsTo, Contents=constraints.Contents, startsIn=constraints.startsIn)
        new_constraints.save()
        return new_constraints
        
#edit a constraint
@router.put("/edit")
def api_edit(C: Constraints):
    filter:Filter = Filter(belongsTo=C.belongsTo, startsIn=C.startsIn)
    constraints: Constraints = api_find_by_name_and_date(filter)
    if constraints == None:
        print("constraints not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        for i in range(len(C.Contents)):
            for n in range(len(C.Contents[i])):
                constraints.Contents[i][n]=C.Contents[i][n]
        constraints.save()
        return constraints
        
#delete a constraint
@router.delete("/delete/{Cid}")
def api_delete(Cid):
    constraints:Constraints = Constraints.get(Cid).run()
    if constraints == None:
        print("constraints not found")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    else:
        constraints.delete()
        return Response(status_code=status.HTTP_200_OK)
    
