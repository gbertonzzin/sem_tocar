"""Handles Gcalendar API requests
PT:Lida com pedidos do Gcalendar API
"""

from datetime import date, datetime, timedelta, time, timezone
from modules.services import get_calendar_service

# from feed.date import rfc3339
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
    logger.debug(f"check_event() - \n    cal_id: {cal_id}\n    event_id: {event_id}")

    with open(f"json\\{cal_name}_today_events.json") as f:
        today_data = json.load(f)
    for event in today_data:
        this_event = today_data[event]
        if event_id == this_event["id"]:
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
                now = datetime.now(timezone.utc).astimezone().isoformat()
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event["end"].get("dateTime", event["end"].get("date"))
                # TFnow = rfc3339.tf_from_timestamp(now)
                # TFstart = rfc3339.tf_from_timestamp(start)
                # TFend = rfc3339.tf_from_timestamp(end)

                if TFstart < TFnow and TFend > TFnow:
                    logger.info("O horário confere")
                    logger.info("Entrada permitida!")
                    return True
                else:
                    logger.info("O horário diverge")
                    logger.info("Entrada negada!")
                    return False
            else:
                logger.info("Evento não encontrado pelo API")
                return False
