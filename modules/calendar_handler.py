"""Handles Gcalendar API requests
PT:Lida com pedidos do Gcalendar API
"""

from datetime import date, datetime, timedelta, time, timezone
from modules.services import get_calendar_service
import os

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
    service = get_calendar_service()
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
    service = get_calendar_service()
    logger.info("Requerindo eventos...")
    events_result = (
        service.events()
        .list(
            calendarId=cal_id,
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


def get_today_events(cal_id):
    logger.debug("get_today_events()")
    
    return get_events(cal_id, 1)


def check_event(cal_id, event_id, cal_name):
    """Checks if event is happening right now
    PT:Verifica se o evento está ocorrento agora

    Args:
        cal_id: Calendar ID
        event_id: Event ID
    Returns:
        Boolean
    """
    logger.debug("check_event()")

    #with open(make_path(f"{cal_name}_today_events.json", "json")) as f:
    with open(os.path.sep.join(["json"] + [f"{cal_name}_today_events.json"])) as f:
        today_data = json.load(f)
    for event_object in today_data.values():
        if event_id == event_object["id"][0:26]:#Watch out for recursive events! Only the first 26 chars matter now
            service = get_calendar_service()
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
                print(now)
                print(start)
                print(end)

                if start <= now < end:
                    logger.info("O horário confere")
                    return True
                else:
                    logger.info("O horário diverge")
                    
            else:
                logger.info("Evento não encontrado pelo API")
                
        else:
            logger.debug(f"{event_id} nao esta no calendario!")
            print(event_id, event_object["id"][0:26])
            


def parse_time_object(tobject):
    return pendulum.parse(tobject["dateTime"]).int_timestamp #.set(tz=pendulum.tz.timezone(tobject["timeZone"]))
