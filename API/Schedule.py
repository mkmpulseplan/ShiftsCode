from fastapi import APIRouter,Response,status
import random
from datetime import date, timedelta
from DAL.Schedule import *
from DAL.Employee import *
from DAL.Shift import *
from DAL.Constraints import *
from DAL.Settings import *
from API.Shift import *
from API.Constraints import *
from API.Settings import *

router = APIRouter(prefix="/Schedule")

# find all
@router.get("/all")
def api_get_all():
    return Schedule.find().run()

#find all by date
@router.get("/find_by_date/{Date}")
def api_get_by_date(Date: date):
    result = Schedule.find().run()
    for S in result:
        if S.startsIn == Date:
            return S

#create new
@router.post("/New")
def api_new_Schedule(allConstraints: List[Constraints]):
    settings = api_find_settings()
    previousSchedule = api_get_by_date(allConstraints[1].startsIn-timedelta(days=7))
    for C in allConstraints:
        employee = Employee.get(C.belongsTo).run()
        if employee == None:
            print("employee not found")
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        else:
            ConstraintsList = []
            OrigEmployeeList = []
            for C in allConstraints:
                ConstraintsList.append(C.Contents)
                OrigEmployeeList.append(C.belongsTo)

    #count shifts in previous schedule
    shifts = previousSchedule.ShiftsSTR
    noLastResort = []
    for n in OrigEmployeeList:
        employee = Employee.get(n).run()
        if employee.isLastResort == False:
            noLastResort.append(n)
    min = 100
    minLST = []
    counter = []
    for i in range(len(noLastResort)):
        counter.append(0)
    for D in range(len(shifts)):
        for E in range(len(shifts[D])):
            for n in range(len(noLastResort)):
                if noLastResort[n]==E:
                    counter[n]+=1
    
    min = counter[0]
    minLST.append(noLastResort[0])
    for amount in range(1,len(counter)):
        if counter[amount]<min:
            min = counter[amount]
            minLST.clear()
            minLST.append(noLastResort[amount])
        if counter[amount]==min:
            minLST.append(noLastResort[amount])


    Days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    ShiftTypes = ["Morning", "Evening", "Night"]

    PreviousFriday = Shift.api_get_by_date(allConstraints[1].startsIn-timedelta(days=2))
    PreviousSaturday = Shift.api_get_by_date(allConstraints[1].startsIn-timedelta(days=1))
    #List of employees who worked in the last 2 shifts
    Previous2Shifts = [PreviousSaturday[-2].belongsTo,PreviousSaturday[-1].belongsTo]
    if settings.ShmoneShmone == False:
        Previous2Shifts.pop(0)
    #List of employees who worked in the last 2 days
    Previous2Days = [[]]
    for i in range(len(PreviousSaturday)):
        Previous2Days[1].append(PreviousSaturday[i].belongsTo)
    for i in range(len(PreviousFriday)):
        Previous2Days[1].append(PreviousFriday[i].belongsTo)

    HoshenStatus = 0
    if "Hoshen" in Previous2Days:
        HoshenStatus=Previous2Days.index("Hoshen")

    SpecialAmitCondition = False
    #add employees to special status lists
    LastResortLST = []
    NationalServiceLST = []
    NeverBreak88LST = []
    for EN in OrigEmployeeList:
        employee = Employee.get(EN).run()
        if employee == None:
            print("employee not found")
            return Response(status_code=status.HTTP_404_NOT_FOUND)
        else:
            if employee.isLastResort == True:
                LastResortLST.append(EN)
            if employee.isNationalService == True:
                NationalServiceLST.append(EN)
            if employee.NeverBreak88 == True:
                NeverBreak88LST.append(EN)

    if settings.TwelveHourShifts == True:
        ShiftsPerDay = 2
    else:
        ShiftsPerDay = 3
    num_days = len(ConstraintsList[0])
    num_employees = len(ConstraintsList)

    WeekSchedule = [["Sunday:"], ["Monday:"], ["Tuesday:"], ["Wednesday:"], ["Thursday:"], ["Friday:"], ["Saturday:"]]
    for currentDay in range(num_days):
        for currentShift in range(ShiftsPerDay):
            #Check if by chance everyone put this specific shift as non available
            b=False
            for ActualStatus in range(num_employees):
                currentAvailability = ConstraintsList[ActualStatus][currentDay][currentShift]
                if currentAvailability != "Unavailable" and currentAvailability != "Cannot":
                    b = True
            if b == False:
                return Response(status_code=status.HTTP_400_BAD_REQUEST)
            
            #if someone already got X shifts, put them later in the favoritsm
            GotEnoughtShifts = []
            ShiftCounter = []
            for i in range(len(OrigEmployeeList)):
                ShiftCounter.append(0)
            for day in WeekSchedule:
                for i in range (len(day)-1):
                    for n in range(len(OrigEmployeeList)):
                        if day[i+1]==OrigEmployeeList[n]:
                            ShiftCounter[n]+=1
            for i in range(len(ShiftCounter)):
                if ShiftCounter[i]>=settings.MinimumShifts:
                    GotEnoughtShifts.append(OrigEmployeeList[i])

            #Resets all lists
            CurrentUnavailable.clear()
            CurrentUnavailable = set(Previous2Shifts)
            FavoredEmployees= []
            AvailableEmployees= []

            #starts with being nice to everyone
            for ActualStatus in range(num_employees):
                currentAvailability = ConstraintsList[ActualStatus][currentDay][currentShift]
                if currentAvailability == "Unavailable" or currentAvailability == "Cannot" or currentAvailability == "Prefers Not" or OrigEmployeeList[ActualStatus] in Previous2Shifts or OrigEmployeeList[ActualStatus] in LastResortLST or OrigEmployeeList[ActualStatus] in GotEnoughtShifts or OrigEmployeeList[ActualStatus]==Previous2Days[0][currentShift] or OrigEmployeeList[ActualStatus]==Previous2Days[1][currentShift]:
                    CurrentUnavailable.add(OrigEmployeeList[ActualStatus])

            #if no one is available, Breaks the shift counter rule
            if len(CurrentUnavailable)==len(OrigEmployeeList):
                CurrentUnavailable.clear()
                CurrentUnavailable = set(Previous2Shifts)
                for ActualStatus in range(num_employees):
                    currentAvailability = ConstraintsList[ActualStatus][currentDay][currentShift]
                    if currentAvailability == "Unavailable" or currentAvailability == "Cannot" or currentAvailability == "Prefers Not" or OrigEmployeeList[ActualStatus] in Previous2Shifts or OrigEmployeeList[ActualStatus] in LastResortLST or OrigEmployeeList[ActualStatus]==Previous2Days[0][currentShift] or OrigEmployeeList[ActualStatus]==Previous2Days[1][currentShift]:
                        CurrentUnavailable.add(OrigEmployeeList[ActualStatus])

            #if no one is available, ignores Prefrences:
            if len(CurrentUnavailable)==len(OrigEmployeeList):
                CurrentUnavailable.clear()
                CurrentUnavailable = set(Previous2Shifts)
                for ActualStatus in range(num_employees):
                    currentAvailability = ConstraintsList[ActualStatus][currentDay][currentShift]
                    if currentAvailability == "Unavailable" or currentAvailability == "Cannot" or OrigEmployeeList[ActualStatus] in Previous2Shifts or OrigEmployeeList[ActualStatus] in LastResortLST or OrigEmployeeList[ActualStatus]==Previous2Days[0][currentShift] or OrigEmployeeList[ActualStatus]==Previous2Days[1][currentShift]:
                        CurrentUnavailable.add(OrigEmployeeList[ActualStatus])

            #if no one is available, ignores no more than 2 same type shifts in a row:
            if len(CurrentUnavailable)==len(OrigEmployeeList):
                CurrentUnavailable.clear()
                CurrentUnavailable = set(Previous2Shifts)
                for ActualStatus in range(num_employees):
                    currentAvailability = ConstraintsList[ActualStatus][currentDay][currentShift]
                    if currentAvailability == "Unavailable" or currentAvailability == "Cannot" or OrigEmployeeList[ActualStatus] in Previous2Shifts or OrigEmployeeList[ActualStatus] in LastResortLST:
                        CurrentUnavailable.add(OrigEmployeeList[ActualStatus])

            #if no one is available, ignores 8-8 rule:
            if len(CurrentUnavailable)==len(OrigEmployeeList):
                CurrentUnavailable.clear()
                Previous2Shifts.pop(0)
                CurrentUnavailable = set(Previous2Shifts)
                for ActualStatus in range(num_employees):
                    currentAvailability = ConstraintsList[ActualStatus][currentDay][currentShift]
                    if currentAvailability == "Unavailable" or currentAvailability == "Cannot" or OrigEmployeeList[ActualStatus] in Previous2Shifts or OrigEmployeeList[ActualStatus] in LastResortLST or OrigEmployeeList[ActualStatus] in NeverBreak88LST:
                        CurrentUnavailable.add(OrigEmployeeList[ActualStatus])

            #if no one is available, backtrack:    
            if len(CurrentUnavailable)==len(OrigEmployeeList):
                CurrentUnavailable.clear()
                CurrentUnavailable = set(Previous2Shifts)
                if day != 0 and len(PreviousAvailable)!=1:
                    #backtracks in the same day
                    if currentShift != 0:
                        PreChosen = random.choice(PreviousAvailable)
                        WeekSchedule[day][currentShift-1]=PreChosen
                        Previous2Days[0][currentShift-1] = Previous2Days[1][currentShift-1]
                        Previous2Days[1][currentShift-1] = PreChosen

                        #Updates the previous 2 shifts
                        Previous2Shifts[-1]=PreChosen

                        CurrentUnavailable.clear()
                        CurrentUnavailable = set(Previous2Shifts)
                        for ActualStatus in range(num_employees):
                            currentAvailability = ConstraintsList[ActualStatus][currentDay][currentShift]
                            if currentAvailability == "Unavailable" or currentAvailability == "Cannot" or OrigEmployeeList[ActualStatus] in Previous2Shifts or OrigEmployeeList[ActualStatus] in LastResortLST:
                                CurrentUnavailable.add(OrigEmployeeList[ActualStatus])
                    #backtracks in 2 different days
                    else:
                        PreChosen = random.choice(PreviousAvailable)
                        WeekSchedule[day-1][-1]=PreChosen
                        Previous2Days[0][currentShift-1] = Previous2Days[1][currentShift-1]
                        Previous2Days[1][currentShift-1] = PreChosen

                        #Updates the previous 2 shifts
                        Previous2Shifts[-1]=PreChosen
                        CurrentUnavailable.clear()
                        CurrentUnavailable = set(Previous2Shifts)
                        for ActualStatus in range(num_employees):
                            currentAvailability = ConstraintsList[ActualStatus][currentDay][currentShift]
                            if currentAvailability == "Unavailable" or currentAvailability == "Cannot" or OrigEmployeeList[ActualStatus] in Previous2Shifts or OrigEmployeeList[ActualStatus] in LastResortLST:
                                CurrentUnavailable.add(OrigEmployeeList[ActualStatus])

            #if no one is available, puts last resort employees
            if len(CurrentUnavailable)==len(OrigEmployeeList):
                CurrentUnavailable.clear()
                CurrentUnavailable = set(Previous2Shifts)
                for ActualStatus in range(num_employees):
                    currentAvailability = ConstraintsList[ActualStatus][currentDay][currentShift]
                    if currentAvailability == "Unavailable" or currentAvailability == "Cannot" or OrigEmployeeList[ActualStatus] in Previous2Shifts:
                        CurrentUnavailable.add(OrigEmployeeList[ActualStatus])
            
            #if still no one is available, return 400 error code
            if len(CurrentUnavailable)==len(OrigEmployeeList):
                print("no one is available")
                return Response(status_code=status.HTTP_400_BAD_REQUEST)

            #creates a favored list
            for ActualStatus in range(num_employees):
                currentAvailability = ConstraintsList[ActualStatus][currentDay][currentShift]
                if (currentAvailability == "Prefers" or (OrigEmployeeList[ActualStatus] in minLST and currentAvailability != "Prefers Not")) and OrigEmployeeList[ActualStatus] not in CurrentUnavailable:
                    FavoredEmployees.append(OrigEmployeeList[ActualStatus])

            for i in range(len(OrigEmployeeList)):
                if OrigEmployeeList[i] not in CurrentUnavailable:
                    AvailableEmployees.append(OrigEmployeeList[i])
            b=False
            if HoshenStatus>0 and "Hoshen" in AvailableEmployees and currentDay==0 and currentShift<=2:
                if HoshenStatus ==1 and currentShift ==1:
                    Chosen = "Hoshen"
                    b=True
                if HoshenStatus ==0 and currentShift ==0:
                    Chosen = "Hoshen"
                    b=True
            if b==False:
                if SpecialAmitCondition == True and currentShift == 0 and "Amit" in AvailableEmployees:
                    Chosen = "Amit"
                    SpecialAmitCondition = False
                if len(FavoredEmployees)!=0:
                    Chosen = random.choice(FavoredEmployees)
                    if Chosen == "Amit" and currentShift == 1:
                        SpecialAmitCondition = True
                elif len(AvailableEmployees)!=0:
                    Chosen = random.choice(AvailableEmployees)
                else:
                    print("Could not create schedule")
                    return Response(status_code=status.HTTP_404_NOT_FOUND)

            #add the employee to the schedule
            WeekSchedule[currentDay].append(Chosen)
            #Updates the previous 2 days
            Previous2Days[0][currentShift] = Previous2Days[1][currentShift]
            Previous2Days[1][currentShift] = Chosen

            #Updates the previous 2 shifts
            Previous2Shifts.append(Chosen)
            if len(Previous2Shifts)>2 or (len(Previous2Shifts)==2 and settings.ShmoneShmone==False):
                Previous2Shifts.pop(0)
            
            #duplicates the available employees for worst case next shift
            PreviousAvailable = []
            for name in AvailableEmployees:
                PreviousAvailable.append(name)
    


    #creates oncall shifts
    OnCallAvailables=[]
    for currentDay in range(num_days):
        for currentShift in range(ShiftsPerDay):
            if currentShift==ShiftsPerDay-1:
                BasicUnavailable = {}
                for ActualStatus in range(num_employees):
                        currentAvailability = ConstraintsList[ActualStatus][currentDay][currentShift]
                        if currentAvailability == "Unavailable" or currentAvailability == "Cannot" or OrigEmployeeList[ActualStatus]==WeekSchedule[day][currentShift-1] or OrigEmployeeList[ActualStatus]==WeekSchedule[day][currentShift-2]:
                            BasicUnavailable.add(OrigEmployeeList[ActualStatus])
                for name in OrigEmployeeList:
                    if name not in BasicUnavailable:
                        OnCallAvailables.append(name)
                if len(OnCallAvailables)!=0:
                    OnCallChosen = random.choice(OnCallAvailables)
                else:
                    OnCallChosen = "N/A"
                WeekSchedule[currentDay].append(OnCallChosen)

    #creates the actual shift collection
    WeekShifts = [[],[],[],[],[],[],[]]
    for currentDay in range(num_days):
        for currentShift in range(ShiftsPerDay):
            newShiftObject:Shift = Shift(belongsTo=WeekSchedule[currentDay][currentShift],Date=allConstraints[0].startsIn, Day=Days[currentDay], Type=ShiftTypes[currentShift])
            WeekShifts[currentDay].append(newShiftObject)
            Shift.api_add_a_shift(newShiftObject)

    #creates the new schedule in the data base
    new_schedule:Schedule = Schedule(startsIn=allConstraints[0].startsIn,ShiftsSTR=WeekSchedule,Shifts=WeekShifts)
    the_schedule:Schedule = api_get_by_date(new_schedule.startsIn) 
    if the_schedule != None:
        the_schedule.delete()
    new_schedule.save()
    return new_schedule


#edit a schedule
@router.put("/edit")
def api_edit(schedule:Schedule):
    the_schedule:Schedule = api_get_by_date(schedule.startsIn) 
    if the_schedule != None:
        the_schedule.delete()
    schedule.save()
    return schedule


#delete a schedule
@router.delete("/delete")
def api_delete(schedule:Schedule):
    the_schedule: Schedule = Schedule.get(schedule.id).run()
    if the_schedule == None:
        print("schedule not found")
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        schedule.delete()
        return Response(status_code=status.HTTP_200_OK)    



