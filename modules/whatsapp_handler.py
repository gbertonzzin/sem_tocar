from modules.sem_tocar_config import *
from modules.toolbox import *
import time
import os
from urllib.parse import quote
import webbrowser as web
import pyautogui as pg

def notify_whatsapp (event):
    for phone_no in event["description"].split(","):
        wait_time = 60
        close_time = 15
        event_time = format_human_date(event['start'])
        message = f"Olá, você tem um evento em {COMPANY_NAME} às {event_time['time']} do dia {event_time['day']} de {event_time['month']} ({event_time['weekday']}), apresente o QR na entrada"
        #phone_no = event["description"]
        image = make_path(f"QR_{event['id']}.png", "QR")
        
        parsed_message = quote(message)
        web.open('https://web.whatsapp.com/send?phone=' +
                phone_no + '&text=' + parsed_message)
        print(message, phone_no)
        time.sleep(wait_time)
        width, height = pg.size()
        pg.click(width/2, height/2)
        time.sleep(wait_time/4)
        pg.press('enter')
        os.system(
        f"xclip -selection clipboard -target image/png -i {image}")
        time.sleep(wait_time/4)
        pg.hotkey("ctrl", "v")
        time.sleep(wait_time/4)
        pg.press('enter')
        
        time.sleep(close_time)
        pg.hotkey("ctrl", "w")