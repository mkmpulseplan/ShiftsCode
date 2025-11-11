from fastapi import FastAPI
import uvicorn
import uvicorn.logging 
from API.Constraints import router as constraints_router
from API.Employee import router as employee_router
from API.MoreBlockRequest import router as blockRequest_router
from API.Schedule import router as schedule_router
from API.Settings import router as settings_router
from API.Shift import router as shift_router
from API.SwitchRequest import router as switchRequest_router
from API.VacationRequest import router as vacationRequest_router
from API.SupportQuery import router as supportQuery_router



app = FastAPI()
app.include_router(constraints_router)
app.include_router(employee_router)
app.include_router(blockRequest_router)
app.include_router(schedule_router)
app.include_router(settings_router)
app.include_router(shift_router)
app.include_router(switchRequest_router)
app.include_router(vacationRequest_router)
app.include_router(supportQuery_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=1948,reload=True)