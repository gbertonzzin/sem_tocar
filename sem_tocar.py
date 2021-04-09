"""
Main controler for the app
PT:Controlador do app
"""
#TODO: multiple calendars, folders for each, etc.
#TODO: config file
#TODO: better GUI
#TODO: printer work


from datetime import date
from os import mkdir
from modules.calendar_handler import *
from modules.JSON_handler import *
from modules.webcam_handler import *
from modules.QR_handler import *
from modules.email_handler import *
from modules.sem_parar_config import *


def main():
    routine()

def routine():
    """
    Establishes routine for the app to execute every so often  PT:
    
    Args:
        None?
    Returns:
        Boolean?
    """
    calendars = get_calendars()         #FLAT IS BETTER THAN NESTED
    if calendars:
        write_json(calendars, f'json\\calendars.json')
        for calendar in calendars:
            if 'selected' in calendars[calendar]:
                cal_id = calendars[calendar]['id'][0:26]
                cal_name = calendars[calendar]['summary']
                file_OK = json_file_check(f'json\\{cal_name}_all_events_new.json', f'json\\{cal_name}_all_events_{date.today()}.json')
                if file_OK:
                    events = get_events(f'{cal_id}@group.calendar.google.com', DAYS_TO_REQUEST)
                    if events:
                        write_json(events, f'json\\{cal_name}_all_events_new.json')
                        new_event = compare_json(f'json\\{cal_name}_all_events_new.json', f'json\\{cal_name}_all_events_{date.today()}.json')
                        if new_event:
                            for event_id in new_event:
                                encrypted = encrypt_data(cal_id, event_id)
                                produce_QR(encrypted, f'QR\\QR_{event_id}.png')             
                                for event in events:                    
                                    if event_id == events[event]['id']: 
                                        if 'attendees' in events[event]:
                                            for attendee in events[event]['attendees']:
                                                print(f"Convidado:{attendee['email']}")
                                                text_message = f'você tem um novo evento: {events[event]["summary"]}'
                                                message = create_message_with_attachment(USER_ID, attendee['email'], events[event]['id'], text_message, f'QR\\QR_{event_id}.png' )
                                                send_message(USER_ID, message)
                                        else:
                                            print('nao ha convidados para esse evento')
                                            print('imprimindo...')
                                    else:
                                        pass
                        else:
                            print('Não há novos eventos!')
                            return False
                else:
                    events = get_events(f'{cal_id}@group.calendar.google.com', 30)
                    if events:
                        write_json(events, f'json\\{cal_name}_all_events_new.json')
                        print(f'File json\\{cal_name}_all_events_new.json created! Try again now.')
                        return False
                    else:
                        print('Não há eventos!')
                        return False

def doorman():
    """
    DOCSTRING PENDING  PT:

    Args:
        None?
    Returns:
        Boolean
    """
    #print(f'doorman()')
    calendars = get_calendars()
    for calendar in calendars:
            if 'selected' in calendars[calendar]:
                cal_id = calendars[calendar]['id'][0:26]
                cal_name = calendars[calendar]['summary']
    today_events = get_today_events(f'{cal_id}@group.calendar.google.com')
    if today_events:
        write_json(today_events, f'json\\{cal_name}_today_events.json')
    else:
        print('Não há eventos hoje!')
        return False

    data = webcam_handler()
    if data:
        decrypted = decrypt_data(data)
        if decrypted:
                check_event(decrypted[0], decrypted[1], cal_name)
        else:
            return False


if __name__ == '__main__':
    main()