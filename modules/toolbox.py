"""
A place for useful functions used all over the app
"""
#from datetime import datetime
import pendulum
import os

def format_human_date(event_start):
    
    pendulum.set_locale('pt_br')

    timestamp = parse_time_object(event_start)
    format_date = pendulum.from_timestamp(timestamp)
    weekday = format_date.format('dddd', locale='pt_br')
    day = format_date.format('DD', locale='pt_br')
    month = format_date.format('MMMM', locale='pt_br')
    year = format_date.format('YYYY', locale='pt_br')
    time = format_date.format('HH:mm', locale='pt_br')
    diff = format_date.diff_for_humans()
    
    human_date = f"{day} de {month} de {year}, {weekday}, às {time}, {diff}"
    
    return human_date
    

def parse_time_object(tobject):
    return pendulum.parse(tobject["dateTime"]).int_timestamp #.set(tz=pendulum.tz.timezone(tobject["timeZone"]))

def make_path(fname, *directories):
    return os.path.sep.join(list(directories) + [fname])