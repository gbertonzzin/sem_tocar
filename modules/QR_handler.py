"""Handles QR code creation, encryption and decoding
PT:Lida com a criptografia, criação e decodificação de QR codes
"""

from cryptography.fernet import Fernet
from itertools import zip_longest
import qrcode

# used for decoding, maybe use qrcode for this as well?
from pyzbar.pyzbar import decode
from PIL import Image


def generate_key():
    """Generates a crypto key and saves it into a file  
    PT:Gera uma chave criptogáfica e salva em um arquivo

    Returns:
        None
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)


def encrypt_data(cal_id, eve_id):
    """Jumbles and encrypts the two inputs given  
    PT:Embaralha e encripta os dois argumentos
    
    Args:
        cal_id:Calendar ID, 26-long string
        eve_id:Event ID, 26-long string
    Returns:
        Encrypted data, 164-long string
    """
    # print(f'encrypt_data - \n    cal_id: {cal_id}, eve_id: {eve_id}')

    filler = ""  # CRYPTO_FILLER, not used
    jumbled = (
        "".join(i for j in zip_longest(cal_id, eve_id, fillvalue=filler) for i in j)
    )[::-1]
    print(f"Embaralhado: {jumbled}")
    key = open("secret.key", "rb").read()
    encoded_message = jumbled.encode()
    f = Fernet(key)
    encrypted = f.encrypt(encoded_message)
    print(encrypted)

    return encrypted


def produce_QR(qrinput, outFile):
    """Generates a QR code and outputs to a PNG file  
    PT:Gera um código QR e salva o arquivo PNG
    
    Args:
        qrinput:Data to be put into the QR
        outFile:Filename for the output

    Returns:
        None
    """
    # print(f'produce_QR')

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qrinput)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(outFile)


def check_QR(file):  # NOT USED, remove?
    """ Reads the provided image file and decodes the QR code if present  
    PT:Lê uma imagem e decodifica o código QR se houver
    
    Args:
        file: .png file to be checked
    Returns:
        Data retrieved from QR code, or False
    """
    # print(f'check_QR() - \n    file: {file}')

    QRdata = decode(Image.open(file))
    if QRdata:
        data = QRdata[0][0].decode("utf-8")
        return data
    else:
        return False


def decrypt_data(input):
    """Decrypts and unjumbles the data provided
    PT:
    
    Args:
        input: data to be decrypted
    Returns:
        Tuple containing the calendar ID and event ID retrieved
    """
    # print(f'decrypt_data() - \n    input: {input}')

    encoded_input = bytes(input, "utf-8")
    key = open("secret.key", "rb").read()
    f = Fernet(key)
    decrypted = f.decrypt(encoded_input).decode()

    # .replace("$","")#for use with CRYPTO_FILLER
    unjumbled_cal_id = (decrypted[1::2])[::-1]
    unjumbled_eve_id = (decrypted[0::2])[::-1]  # .replace("$","")
    print("cal ID: ", unjumbled_cal_id, " | event ID: ", unjumbled_eve_id)

    return unjumbled_cal_id, unjumbled_eve_id
