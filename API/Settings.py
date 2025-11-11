from fastapi import APIRouter,Response,status
from DAL.Settings import *

router = APIRouter(prefix="/settings")

#find the settings object
@router.get("/find")
def api_find_settings():
    return (Settings.find().run())[0]

@router.put("/edit")
def api_edit_settings(settings: Settings):
    existing_settings = api_find_settings()

    existing_settings.TwelveHourShifts = settings.TwelveHourShifts
    existing_settings.MinimumShifts = settings.MinimumShifts
    existing_settings.ShmoneShmone = settings.ShmoneShmone
    existing_settings.Max2ShiftsSameType = settings.Max2ShiftsSameType

    existing_settings.save()
    return existing_settings


@router.put("/reset")
def api_reset_settings():
    existing_settings = api_find_settings()

    existing_settings.TwelveHourShifts = False
    existing_settings.MinimumShifts = 2
    existing_settings.ShmoneShmone = True
    existing_settings.Max2ShiftsSameType = True

    existing_settings.save()
    return existing_settings