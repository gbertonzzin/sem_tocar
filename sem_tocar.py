"""
Main controler for the app
PT:Controlador do app
"""
import json
import coloredlogs, logging
import threading
import shutil

from time import sleep
from datetime import date
from modules.calendar_handler import *
from modules.JSON_handler import *
from modules.webcam_handler import *
from modules.QR_handler import *
from modules.email_handler import *
from modules.sem_tocar_config import *
from modules.gpio_handler import *
from modules.whatsapp_handler import *
from modules.sms_handler import *
from modules.toolbox import *

logging.basicConfig(filename=f"logs//Log_{date.today()}.txt", 
                    level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
coloredlogs.install(level='DEBUG')

logger = logging.getLogger(__name__)

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.INFO)
logging.getLogger("googleapiclient.discovery").setLevel(logging.INFO)

def main():
    routine_thread = threading.Thread(target=routine, daemon=False)
    doorman_thread = threading.Thread(target=sentry_box)
  
    routine_thread.start()
    sleep(15)
    doorman_thread.start()

def setup():
    """
    Creates the token files for the Gcal and Gmail API and the crypto key file for QR encryption
    """
    logger.info("Verificando arquivos essenciais...")
    if ENCRYPTION == True :
        if os.path.isfile("crypto.key"):
            logger.info("O arquivo de chave de criptografia já existe!")
        else:
            logger.warning("Arquivo de chave de criptografia não encontrado.")
            if os.path.isfile("crypto_backup.key"):
                logger.info("Encontrado arquivo de backup da chave de criptografia.")
                logger.info("Restaurando backup...")
                shutil.copy("crypto_backup.key", "crypto.key")
            else:
                logger.warning("Não encontrado arquivo de backup da chave de criptografia.")
                logger.info("Gerando chave de criptografia 'crypto.key'...")
                generate_key()
        
    if os.path.isfile("gcal_token"):
        logger.info("O token de acesso ao GCalendar já existe!")
    else:
        logger.warning("O token de acesso ao GCalendar não foi encontrado!")
        logger.info("Autenticando o Gcal API...")
        get_service('calendar')
    
    if os.path.isfile("gmail_token"):
        logger.info("O token de acesso ao GMail já existe!")
    else:
        logger.warning("O token de acesso ao GMail não foi encontrado!")
        logger.info("Autenticando o Gmail API...")
        get_service('gmail.send')
        

def sentry_box():       #TODO: What happens when the doorman fails?
    try:                #for example, if the webcam is broken or disconnected
        while True:     #or if the API requests fail? or if some malicious QR is shown?
            doorman()   #the app needs to handle the errors and keep trying doorman without messing with the routine
    except Exception as e:
        problem_found()
        logger.warning(f"Doorman parou: {e}")
        pass


def routine():
    """
    Establishes routine for the app to execute every so often  PT:

    Args:
        None?
    Returns:
        Boolean?
    """
    logger.debug("routine()")
    
    try:
        while True:
            request_calendars()
            sleep(ROUTINE_FREQ)
    except KeyboardInterrupt:
        pass
        

  
    
def request_calendars():
    """
    Requests all user calendars and hands the ones actively selected over to be processed
    
    """
    logger.debug("request_calendars()")
    
    try:
        calendars = get_calendars()
        print(calendars)
    except: 
        logger.warning("Ocorreu um erro ao requisitar os calendários.")
        return False

    if calendars:
        json.dump(calendars, open(make_path("calendars.json", "json"), "wt"))
        for calendar in calendars.values():
            if "selected" in calendar:
                get_today_events(calendar["id"][0:26])
                process_calendar(calendar)
    else:
        logger.warning("Ocorreu um erro ao requisitar os calendários.")


def process_calendar(calendar):
    """
    Coordinates most of the calendar action, checks files, makes requests etc.
    PT: Coordena a maior parte das ações de calendário, checa arquivos, faz requests etc.
    
    """
    logger.debug("process_calendar()")
    
    cal_id = calendar["id"][0:26]
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
                pass
                #notify_whatsapp(event)

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
    

    data = webcam_handler()
    if data:        #NEEDS EXCEPTION HANDLING
        decrypted = decrypt_data(data)
    else:
        logger.warning("Erro crítico!")
        return False
        
    if decrypted:
        
        cal_name = get_calendar(decrypted[0])["summary"]
        if cal_name:
            logger.info(f"Verificando autenticacão para o evento '{cal_name}'.")
            auth_entrance = check_event(decrypted[0], decrypted[1], cal_name)
        else:
            logger.warning(f"O calendário {decrypted[0]} não foi encontrado!")
    else:
        return False
    
    if auth_entrance:
        logger.critical("Entrada permitida!")
        entrance_allowed()
        unlock()
        return True
    else:
        logger.critical("Entrada negada!")
        entrance_not_allowed()
        return True


if __name__ == "__main__":
    main()
