"""Handles email formatting, creation and sending
PT:Lida com a formatação, criação e envio de e-mails
"""
from modules.calendar_handler import *
#from __future__ import print_function
import logging
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
import mimetypes
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from googleapiclient.errors import HttpError
from modules.services import *
from modules.sem_tocar_config import *

logger = logging.getLogger(__name__)


def create_message_with_attachment(sender, to, subject, message_text, file):
    """Creates a message for email with an attachment
        PT:

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.
        file: The path to the file to be attached.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = "application/octet-stream"

    main_type, sub_type = content_type.split("/", 1)

    if main_type == "text":
        fp = open(file, "rb")
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == "image":
        fp = open(file, "rb")
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(file, "rb")
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()

    filename = os.path.basename(file)
    msg.add_header("Content-Disposition", "attachment", filename=filename)
    message.attach(msg)

    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {"raw": raw}

    return body


def send_message(message):
    """Send an email message
    PT:

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    service = get_service('gmail')
    try:
        message = (
            service.users().messages().send(userId=USER_ID, body=message).execute()
        )
        logger.info("E-mail enviado!")
        logger.info("ID da mensagem e-mail: %s" % message["id"])
        return message
    except HttpError as error:
        logger.error("Ocorreu um erro:: %s" % error, exc_info=True)


def notify_attendees(event): #TODO: check if e-mail was sent and received succesfully. Is it even possible?
    """
    Sends the e-mail with the pertinent info and the QR code attached
    PT: Envia o e-mail com as informações pertinentes e o QR code em anexo
    Args:
        event: Event object
    Returns:
        Boolean
    """
    logger.debug("notify_attendees()")
    for attendee in event["attendees"]:
        logger.info(f"Convidado:{attendee['email']}")
        date = format_human_date(event['start'])
        human_date = f"{date['day']} de {date['month']} de {date['year']}, {date['weekday']}, às {date['time']}, {date['diff']}"
        text_message = f"Você tem um novo evento: {event['summary']} em {COMPANY_NAME}, {human_date}, para entrar apresente o código QR em anexo abaixo na portaria e em caso de duvidas favor contactar no telefone {CONTACT_PHONE}."
        message = create_message_with_attachment(
            USER_ID,
            attendee["email"],
            event["summary"],
            text_message,
            make_path(f"QR_{event['id']}.png", "QR"),
        )
        try:
            send_message(message)
        except:
            logger.warning("Ocorreu um erro ao enviar o e-mail!")
    message_ = create_message_with_attachment( #send a copy of the e-mail to the user
        USER_ID,
        USER_ID,
        event["summary"],
        text_message,
        make_path(f"QR_{event['id']}.png", "QR"),
    )
    try:
        send_message(message_)
    except:
        logger.warning("Ocorreu um erro ao enviar o e-mail!")


