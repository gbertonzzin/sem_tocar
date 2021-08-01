"""Handles webcam work
PT:Lida com a webcam
"""
import logging
import cv2
import time
import datetime
import time as t
import argparse
from pyzbar.pyzbar import decode, ZBarSymbol
from modules.sem_tocar_config import *
from modules.calendar_handler import *

logger = logging.getLogger(__name__)


def decoder(image):
    """Tries to find and decode a QR code in the image
    PT:Tenta encontrar e decodificar um código QR na imagem

    Args:
        image:The image to be handled

    Returns:
        The retrieved data from QR code
    """
    #logger.debug("decoder()") Oh, HELL NAW!

    gray_img = cv2.cvtColor(image, 0)
    barcode = decode(gray_img, symbols=[ZBarSymbol.QRCODE])

    for obj in barcode:
        qr_data = obj.data.decode("utf-8")
        #barcodeType = obj.type
        qr_logger(qr_data, image)
        t.sleep(3)

        if len(qr_data) == 164:
            return qr_data
        else:
            logger.warning("Dados do QR inválidos!")
            return False


def qr_logger(data, image):     #TODO
    """Saves the QR image and logs it
    PT:Salva a imagem QR e guarda logs

    Args:
        data:Data encoded on the QR
        image:The QR image

    Returns:
        None
    """
    logger.debug("qr_logger()")

    timestampStr = datetime.now().strftime("%d%m%Y_%H%M%S")

    if SAVE_WEBCAM == True:
        cv2.imwrite(make_path("{timestampStr}.png", "img"), image)
        
    #TODO: log webcam info into JSON for security purposes

def webcam_handler_alternative(): 
    
    cap = cv2.VideoCapture(0)

    
    detector = cv2.QRCodeDetector()
    
    while True:
        ret, frame = cap.read()
        cv2.imshow("Image", frame)
        data, vertices_array, _ = detector.detectAndDecode(frame)
        print("BATATA BAROA", data)
        if vertices_array is not None:
            if data:
                #cv2.destroyAllWindows()
                #del cap
                print(data)
                #return data
        code = cv2.waitKey(10)
        if code == ord("q"):
            cv2.destroyAllWindows()
            del cap
            break
    
def webcam_handler():
    """Turns the camera on and sends each frame to the decoder
    PT:Liga a câmera e envia cada frame para o decoder

    Returns:
        data:encrypted data retrieved from QR code
    """
    logger.debug("webcam_handler()")

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow("Image", frame)
        data = decoder(frame)
        if isinstance(data, str):
            cv2.destroyAllWindows()
            del cap
            return data
        code = cv2.waitKey(10)
        if code == ord("q"):
            cv2.destroyAllWindows()
            del cap
            break
