import json
import coloredlogs, logging
import threading
import shutil

from time import sleep
from datetime import date
from modules.calendar_handler import *
from modules.JSON_handler import *
from modules.QR_handler import encrypt_data, produce_QR
from modules.email_handler import *
from modules.sem_tocar_config import *
from modules.whatsapp_handler import *
from modules.sms_handler import *
from modules.toolbox import *

logging.basicConfig(filename=f"logs//Log_{date.today()}.txt", 
                    level=logging.DEBUG, 
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
coloredlogs.install(level='DEBUG')

logger = logging.getLogger(__name__)

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.INFO)
logging.getLogger("googleapiclient.discovery").setLevel(logging.INFO)

def main():
    request_calendars()

    
def request_calendars():
    """
    Requests all user calendars and hands the ones actively selected over to be processed
    
    """
    logger.debug("request_calendars()")
    
    try:
        calendars = get_calendars()
    except: 
        logger.warning("Ocorreu um erro ao requisitar os calendários.")
        return False

    if calendars:
        json.dump(calendars, open(make_path("calendars.json", "json"), "wt"))
        for calendar in calendars.values():
            if "selected" in calendar:
                cal_id = calendar["id"][0:64]
                cal_name = calendar["summary"]
                print(cal_id, cal_name)

                get_today_events(cal_id, cal_name)
                process_calendar(calendar)
    else:
        logger.warning("Ocorreu um erro ao requisitar os calendários.")


def process_calendar(calendar):
    """
    Coordinates most of the calendar action, checks files, makes requests etc.
    PT: Coordena a maior parte das ações de calendário, checa arquivos, faz requests etc.
    
    """
    logger.debug("process_calendar()")
    
    cal_id = calendar["id"][0:64]
    cal_name = calendar["summary"]
    logger.info(f"Processando calendário: {cal_name}")
    
    file_OK = json_file_check(
        make_path(f"{cal_name}_all_events_new.json", "json"),
        make_path(f"{cal_name}_all_events_{date.today()}.json", "json"),
        )
    
    events = get_events(cal_id, DAYS_TO_REQUEST, False)
    
    with open(make_path(f"{cal_name}_all_events_new.json", "json"), "w") as file:
        file.write(json.dumps(events, indent=4, sort_keys=True))
    if events:
        logger.info(f"Há eventos no calendário {cal_name}!")
    else:
        logger.info(f"Não há eventos no calendário {cal_name}!")
    
    if file_OK == True:
        
        
        new_event = compare_json(
            make_path(f"{cal_name}_all_events_new.json", "json"),
            make_path(f"{cal_name}_all_events_{date.today()}.json", "json"),
        )
            
        if new_event:
            for event_id in new_event:
                process_new_events(cal_id, event_id, events)
        else:
            logger.info(f"Não há novos eventos no calendário {cal_name}!")
            return False
    else:
        logger.warning(f"Ocorreu um erro. Tentando novamente em {ROUTINE_FREQ} segundos.")
        logger.warning("AVISO: Se houverem eventos no calendário, não serão considerados como novos!")
    
#FIX: if there is no '_all_events_new.json', a new one will be created containing the already existing events.
#This is a problem because if the file gets deleted or corrupted before a new event is notified, then this event
#   will never get notified since comparing the last and new requests will yeld no new events 
#   (they are the same, the last is just the new one renamed. Maybe change this?)
#Not sure how to tackle this, since we also do not want events getting notified twice (well, better twice than never?)
#Maybe a separate database with all the alredy-notified events? Pain in the ass.


def process_new_events(calendar_id, event_id, events):
    """
    Coordinates QRs and notifying for new events through e-mail
    PT: Coordena QRs e notificação dos novos eventos através de e-mail
    """
    logger.debug("process_new_events()")
    
    encrypted = encrypt_data(calendar_id, event_id)
    produce_QR(encrypted, make_path(f"QR_{event_id}.png", "QR"))
    for event in events.values():
        if event_id == event["id"]:
            if "attendees" in event:
                notify_attendees(event)
            else:
                logger.info("Não há convidados para esse evento!")
                
                if PRINT_INVITE == True:
                    logger.info("Imprimindo...")
                    #invite = write_invitation(event, make_path(f"QR_{event_id}.png", COMPANY_NAME, "QR"))
                    #op_sys = platform.system()
                    #if op_sys == 'Windows':
                    #   win_print_doc(invite)
                    #elif op_sys == 'Linux':
                    #   linux_print_doc(invite)
                    #else:
                    #   logger.warning("Não foi possível determinar o sistema operacional!")
            if "description" in event:
                notify_whatsapp(event)


if __name__ == "__main__":
    main()
