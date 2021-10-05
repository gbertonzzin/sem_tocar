from modules.sem_tocar_config import *
from modules.toolbox import *
import pywhatkit

def test_whatsapp():
    
    phone = "+5514981605496"
    img = "teste.png"
    
    text_message = f"ATENÇÃO CHEGOU CHATUBA HEIN"
    img_caption = ""
    
    #im = Image.open(img)
    #im.show()

    pywhatkit.sendwhats_image(phone, img, img_caption, 30, True, 5)

def notify_whatsapp(event):
    
    pendulum.set_locale('pt_br')

    phone = event['description']
    img = make_path(f"QR_{event['id']}.png", "/home/pi/Desktop/app/venv/sem_tocar/QR")
    
    text_message = f"Você tem um evento em {COMPANY_NAME}, {format_human_date(event['start'])}, em caso de duvidas favor contactar no telefone {CONTACT_PHONE}"
    img_message = f"Apresente este código à webcam na entrada para destrancar a porta."
    
    #print(text_message)
    #pywhatkit.sendwhatmsg_instantly(phone, text_message, 40, False, 1)

    pywhatkit.sendwhats_image(phone, img, "", 15, True, 1)



def send_wapp_message():
    pywhatkit.check_window()
    
    pass

def send_wapp_image():
    pass