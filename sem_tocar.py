"""
Main controler for the app
PT:Controlador do app
"""
import json
import logging

# TODO: multiple calendars, folders for each, etc.
# TODO: config file
# TODO: better GUI
# TODO: printer work


from datetime import date
from modules.calendar_handler import *
from modules.JSON_handler import *
from modules.webcam_handler import *
from modules.QR_handler import *
from modules.email_handler import *
from modules.sem_tocar_config import *


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


def main():
    routine()

def setup():
    """
    Creates the token files for the Gcal and Gmail API and the crypto key file for QR encryption
    """
    
    generate_key()
    
def make_path(fname, *directories):
    return os.path.sep.join(list(directories) + [fname])

def routine():
    """
    Establishes routine for the app to execute every so often  PT:

    Args:
        None?
    Returns:
        Boolean?
    """
    calendars = get_calendars() 
    if calendars:
        json.dump(calendars, open(make_path("calendars.json", "json"), "wt"))
        for calendar in calendars.values():
            if "selected" in calendar:
                process_calendar(calendar)


def process_calendar(calendar):
    cal_id = calendar["id"][0:26]
    cal_name = calendar["summary"]
    file_OK = json_file_check(
        make_path(f"{cal_name}_all_events_new.json", "json"),
        make_path(f"{cal_name}_all_events_{date.today()}.json", "json"),
    )

    events = get_events(f"{cal_id}@group.calendar.google.com", DAYS_TO_REQUEST)
    if events:
        #write_json(events, make_path(f"{cal_name}_all_events_new.json", "json"))
        with open(make_path(f"{cal_name}_all_events_new.json", "json"), "w") as file:
            file.write(json.dumps(events, indent=4, sort_keys=True))
            
        if file_OK:
            new_event = compare_json(
                make_path(f"{cal_name}_all_events_new.json", "json"),
                make_path(f"{cal_name}_all_events_{date.today()}.json", "json"),
            )
            if new_event:
                for event_id in new_event:
                    process_new_events(cal_id, event_id, events)
            else:
                logger.info("Não há novos eventos!")
                return False
        else:
            logger.info("Há problemas com o banco de dados! Tente novamente.")
    else:
        logger.info("Não há eventos!")
        return False


def process_new_events(calendar_id, event_id, events):
    encrypted = encrypt_data(calendar_id, event_id)
    produce_QR(encrypted, make_path(f"QR_{event_id}.png", "QR"))
    for event in events.values():
        if event_id == event["id"]:
            if "attendees" in event:
                notify_attendees(event)
            else:
                logger.info("Não há convidados para esse evento!")
                logger.info("Imprimindo...")


def notify_attendees(event): #TODO: check if e-mail was sent and received succesfully
    """
    Sends the e-mail with the pertinent info and the QR code attached
    PT: Envia o e-mail com as informações pertinentes e o QR code em anexo
    Args:
        event: Event object
    Returns:
        Boolean
    """
    for attendee in event["attendees"]:
        logger.info(f"Convidado:{attendee['email']}")
        text_message = f'você tem um novo evento: {event["summary"]}'
        message = create_message_with_attachment(
            USER_ID,
            attendee["email"],
            event["id"],
            text_message,
            make_path(f"QR_{event['id']}.png", "QR"),
        )
        send_message(USER_ID, message)


def doorman():
    """
    Checks for events happening in the current day and handles the webcam authentication through QR codes
    PT: Checa os eventos acontecendo no dia atual e cuida da autenticação através de QR codes

    Args:
        None?
    Returns:
        Boolean
    """
    logger.debug("doorman()")
    calendars = get_calendars()
    for calendar in calendars:
        if "selected" in calendars[calendar]:
            cal_id = calendars[calendar]["id"][0:26]
            cal_name = calendars[calendar]["summary"]
    today_events = get_today_events(f"{cal_id}@group.calendar.google.com")
    if today_events:
        #write_json(today_events, make_path(f"{cal_name}_today_events.json", "json"))
        with open(make_path(f"{cal_name}_today_events.json", "json"), "w") as file:
            file.write(json.dumps(today_events, indent=4, sort_keys=True))
        
    else:
        logger.info("Não há eventos hoje!")
        return False

    data = webcam_handler()
    if data:
        decrypted = decrypt_data(data)
        if decrypted:
            check_event(decrypted[0], decrypted[1], cal_name)
            if check_event:
                logger.info("Entrada permitida!")
                return True
            else:
                logger.info("Entrada negada!")
                return False
        else:
            return False


if __name__ == "__main__":
    main()
