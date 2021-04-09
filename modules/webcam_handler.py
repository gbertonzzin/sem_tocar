"""Handles webcam work
PT:Lida com a webcam
"""

import cv2
import time
import datetime
import argparse
from datetime import timezone #will it me necessary?
from pyzbar.pyzbar import decode, ZBarSymbol
from modules.sem_parar_config import *

def decoder(image):
    """Tries to find and decode a QR code in the image
    PT:Tenta encontrar e decodificar um código QR na imagem

    Args:
        image:The image to be handled
    
    Returns:
        The retrieved data from QR code
    """

    gray_img = cv2.cvtColor(image,0)
    barcode = decode(gray_img, symbols=[ZBarSymbol.QRCODE])

    for obj in barcode:
        qr_data = obj.data.decode("utf-8")
        barcodeType = obj.type        
        qr_logger(qr_data, image)
        time.sleep(3)

        if len(qr_data) == 164:
            return qr_data
    

def qr_logger(data, image):
    """Saves the QR image and logs it to a .csv
    PT:Salva a imagem QR e loga em um .csv

    Args:
        data:Data encoded on the QR
        image:The QR image

    Returns:
        None
    """
    #print('qr_logger()')

    timestampStr = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")

    if SAVE_WEBCAM == True:
        cv2.imwrite(f'img\\img{timestampStr}.png', image)

    ap = argparse.ArgumentParser()								
    ap.add_argument("-o", "--output", type=str, default="QR_logs.csv", help="")#not logging correctly, change to JSON
    args = vars(ap.parse_args())
    csv = open(args["output"], "w")										
    found = set()
    if data not in found:							
        csv.write(f"{timestampStr}-{data}\n")		
        csv.flush()
        found.add(data)

def webcam_handler():
    """Turns the camera on and sends each frame to the decoder  
    PT:Liga a câmera e envia cada frame para o decoder
    
    Returns:
        data:encrypted data retrieved from QR code
    """
    #print('webcam_handler()')
    
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = cap.read()
        data = decoder(frame)
        cv2.imshow('Image', frame)
        if isinstance(data, str):
            cv2.destroyAllWindows()
            del(cap)
            return data
        code = cv2.waitKey(10)
        if code == ord('q'):
            cv2.destroyAllWindows()
            del(cap)
            break