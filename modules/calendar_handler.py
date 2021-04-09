"""Handles Gcalendar API requests
PT:Lida com pedidos do Gcalendar API
"""

from datetime import date, datetime, timedelta, time, timezone
from modules.services import get_calendar_service
from feed.date import rfc3339
import json

def get_calendars():
    """Requests all calendars from the user
    PT:Pede todos os calendários do usuário

    Returns:
        A dict with the calendars, or False
    """
    all_calendars = {}
    service = get_calendar_service()
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])
    if calendars:
        for i, calendar in enumerate(calendars):
            all_calendars[i] = calendar
        return all_calendars
    else:
        print('Nâo há calendários!')
        return False


def get_events(cal_id, days_future):
    """Requests future non-recursive events up to a number of days  
    PT: Pede os eventos não-recursivos tantos dias no futuro
    
    Args:
        cal_id:Calendar ID
        days_future: How many days to fetch
    Returns:
        A dict with the events, or False
    """
    #print(f'get_events() - \n    cal_id: {cal_id}  days_future: {days_future}')
    
    today_start = datetime.combine(date.today(), time()).astimezone().isoformat()
    max_days = datetime.combine(date.today()+timedelta(days = days_future), time()).astimezone().isoformat()
    all_events = {}
    service = get_calendar_service()
    events_result = service.events().list(calendarId=cal_id, timeMin=today_start, timeMax=max_days, maxResults=2500, singleEvents=False, orderBy='updated').execute()
    events = events_result.get('items', [])

    if events:
        for i, event in enumerate(events):
            all_events[i] = event
        return all_events
    else:
        return False
        print('Não há eventos!')

def get_today_events(cal_id):
    """Requests all events expected for the current day  
    PT: Pede os eventos do dia atual
    
    Args:
        cal_id: Calendar ID
    Returns:
        A dict with the events, or False
    """
    #print(f'get_today_events() - \n    cal_id: {cal_id}')

    today_start = datetime.combine(date.today(), time()).astimezone().isoformat()
    today_end = datetime.combine(date.today()+timedelta(days = 1), time()).astimezone().isoformat()
    all_events = {}
    service = get_calendar_service()
    events_result = service.events().list(calendarId=cal_id, timeMin=today_start, timeMax=today_end, maxResults=2500, singleEvents=True, orderBy='updated').execute()
    
    events = events_result.get('items', [])
    if events:    
        for i, event in enumerate(events):
            all_events[i] = event
        return all_events
    else:
        print('Não há eventos hoje!')
        return False

def check_event(cal_id, event_id, cal_name):
    """Checks if event is happening right now  
    PT:Verifica se o evento está ocorrento agora
    
    Args:
        cal_id: Calendar ID
        event_id: Event ID
    Returns:
        Boolean
    """
    #print(f'check_event() - \n    cal_id: {cal_id}\n    event_id: {event_id}')


    with open(f'json\\{cal_name}_today_events.json') as f:
        today_data = json.load(f)
    for event in today_data:
        this_event = today_data[event]
        if event_id == this_event['id']:
            service = get_calendar_service()
            event = service.events().get(calendarId = f'{cal_id}@group.calendar.google.com', eventId= this_event['id']).execute()
            if event:
                now = datetime.now(timezone.utc).astimezone().isoformat()
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                TFnow = rfc3339.tf_from_timestamp(now)
                TFstart = rfc3339.tf_from_timestamp(start)
                TFend = rfc3339.tf_from_timestamp(end)

                if TFstart < TFnow and TFend > TFnow:
                    print('O horário confere \n Entrada permitida!')
                    return True
                else:
                    print('O horário diverge \n Entrada negada!')
                    return False
            else:
                print('Evento não encontrado pelo API')
                return False