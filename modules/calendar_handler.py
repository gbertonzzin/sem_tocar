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
    service = get_calendar_service()
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get("items", [])
    logger.debug(f"{calendars=}")
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
    logger.debug(f"get_events() - \n    cal_id: {cal_id}  days_future: {days_future}")

    today_start = datetime.combine(date.today(), time()).astimezone()
    max_days = today_start + timedelta(days=days_future)
    service = get_calendar_service()
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
    logger.debug(f"check_event() - {cal_id=} - {event_id=}")

    #with open(make_path(f"{cal_name}_today_events.json", "json")) as f:
    with open(os.path.sep.join("json" + f"{cal_name}_today_events.json")) as f:
        today_data = json.load(f)
    if event_id not in today_data:
        logger.debug(f"{event_id=} nao esta no calendario!")
        return False
    else:
        this_event = today_data[event_id]
        service = get_calendar_service()
        event = (
            service.events()
            .get(
                calendarId=f"{cal_id}@group.calendar.google.com",
                eventId=this_event["id"],
            )
            .execute()
        )
        if event:
            now = pendulum.now().utcnow()
            start = parse_time_object(event["start"]).in_tz("UTC")
            end = parse_time_object(event["end"]).in_tz("UTC")

            if start <= now < end:
                logger.info("O horário confere")
                return True
            else:
                logger.info("O horário diverge")
                return False
        else:
            logger.info("Evento não encontrado pelo API")
            return False


def parse_time_object(tobject):
    key = "dateTime"
    if "date" in tobject:
        key = "date"
    return pendulum.parse(tobject[key]).set(
        tz=pendulum.tz.timezone(tobject["timeZone"])
    )
