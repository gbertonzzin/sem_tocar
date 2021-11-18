"""Handles Gcalendar API requests
PT:Lida com pedidos do Gcalendar API
"""
#import os

from datetime import date, datetime, timedelta, time, timezone
from modules.services import get_service
from modules.toolbox import *


import pendulum
import json
import logging

logger = logging.getLogger(__name__)



def get_calendars():
    """Requests all calendars from the user
    PT:Pede todos os calendários do usuário

    Returns:
        A dict with the calendars, or False
    """
    logger.debug("get_calendars()")
    
    logger.info("Requerindo eventos...")
    try:
        service = get_service('gcal')
    except:
        logger.warning("Servidor não encontrado. O dispositivo está conectado à internet?")
        return False
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get("items", [])
    #logger.debug(f"{calendars=}")
    return {i: calendar for i, calendar in enumerate(calendars)}


def get_events(cal_id, days_future):
    """Requests future non-recursive events up to a number of days
    PT: Pede os eventos não-recursivos tantos dias no futuro

    Args:
        cal_id:Calendar ID
        days_future: How many days to fetch
    Returns:
        A dict with the events, or False
    """
    logger.debug(f"get_events()")

    today_start = datetime.combine(date.today(), time()).astimezone()
    max_days = today_start + timedelta(days=days_future)
    service = get_service('gcal')
    logger.info("Requerindo eventos...")
    events_result = (
        service.events()
        .list(
            calendarId=f"{cal_id}@group.calendar.google.com",
            timeMin=today_start.isoformat(),
            timeMax=max_days.isoformat(),
            maxResults=2500,
            singleEvents=False,
            orderBy="updated",
        )
        .execute()
    )
    events = events_result.get("items", [])

    return {i: event for i, event in enumerate(events)}

def get_calendar(cal_id):
    service = get_service('gcal')
    calendar = service.calendars().get(calendarId=f"{cal_id}@group.calendar.google.com").execute()
    return calendar

def get_today_events(cal_id):
    logger.debug("get_today_events()")
    
    calendars = get_calendars()
    for calendar in calendars:
        if "selected" in calendars[calendar]:
            cal_id = calendars[calendar]["id"][0:26]
            cal_name = calendars[calendar]["summary"]
            logger.info(f"Buscando eventos de hoje para {cal_name}.")
            today_events = get_events(cal_id, 1)
                #write_json(today_events, make_path(f"{cal_name}_today_events.json", "json"))
            with open(make_path(f"{cal_name}_today_events.json", "json"), "w") as file:
                file.write(json.dumps(today_events, 
                                    indent=4, 
                                    sort_keys=True))
            if today_events:
                logger.info(f"Há eventos hoje para o calendário {cal_name}!")

            else:
                logger.info(f"Não há eventos hoje para o calendário {cal_name}!")

def check_event(cal_id, event_id, cal_name):
    """Checks if event is happening right now
    PT:Verifica se o evento está ocorrendo agora

    Args:
        cal_id: Calendar ID
        event_id: Event ID
    Returns:
        Boolean
    """
    logger.debug("check_event()")
    
    with open(make_path(f"{cal_name}_today_events.json", "json")) as f:
    #with open(os.path.sep.join(["json"] + [f"{cal_name}_today_events.json"])) as f:
        today_data = json.load(f)
    for event_object in today_data.values():
        if event_id == event_object["id"][0:26]:#Watch out for recursive events! Only the first 26 chars matter now
            service = get_service('gcal')
            event = (
                service.events()
                .get(
                    calendarId=f"{cal_id}@group.calendar.google.com",
                    eventId=event_object["id"], #Gotta use the database id and not the given id
                )                               #in case it is a recursive event (with all that time junk at the end)
                .execute()
            )
            if event:
                #now = pendulum.now().utcnow().in_tz("America/Sao_Paulo")
                #start = parse_time_object(event["start"]).in_tz("UTC")
                #end = parse_time_object(event["end"]).in_tz("UTC")
                now = pendulum.now().int_timestamp
                start = parse_time_object(event["start"])
                end = parse_time_object(event["end"])
                #print(now)
                #print(start)
                #print(end)

                if (start-(TOLERANCE*60)) <= now < end:
                    if int(start/60) > int(now/60):
                        logger.info(f"O horário confere: {int((start-now)/60)} minutos adiantado.")
                    elif int(start/60) == int(now/60):
                        logger.info("Caraca o cara chegou no exato minuto!")
                    elif int(start/60) < int(now/60):
                        logger.info(f"O horário confere: {int((now-start)/60)} minutos atrasado")
                    return True
                else:
                    logger.info("O horário diverge.")
                    
            else:
                logger.info("Evento não encontrado!")#is it, always?
                
        else:
            logger.info(f"{event_id} nao esta no calendario!")
            #print(event_id, event_object["id"][0:26])
            
