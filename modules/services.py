import logging
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
#from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)

#if "GOOGLE_CREDENTIALS_FILE" not in os.environ:
#    raise KeyError("Environment variable GOOGLE_CREDENTIALS_FILE not defined!")
#google_credentials = os.environ["GOOGLE_CREDENTIALS_FILE"]
google_credentials = "credentials.json"

def authenticate(scope, token):
    creds = None

    if os.path.exists(token):
        with open(token, "rb") as token_file:
            creds = pickle.load(token_file)
    else:
        logger.debug(f"{token} for {scope} not found! Creating...")
        

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(google_credentials, scope)
            creds = flow.run_local_server(port=0)

        with open(token, "wb") as token_file:
            pickle.dump(creds, token_file)

    return creds


def get_calendar_service():
    """Provides Gcalendar API auth and service
    PT:Lida com autenticação e serviços do Gcalendar API

    Returns:
        Gcalendar API service
    """
    logger.debug("get_calendar_service()")


    creds = authenticate(["https://www.googleapis.com/auth/calendar"], "gcal_token")
    if not creds:
        raise ValueError("Houve um erro na autenticação do GCal API!")
    service = build("calendar", "v3", credentials=creds)
    return service


def get_gmail_service():
    """Provides Gmail API auth and service
    PT:Lida com autenticação e serviços do GMail API

    Returns:
        Gmail API service
    """
    logger.debug("get_gmail_service()")
    
    creds = authenticate(["https://www.googleapis.com/auth/gmail.send"], "gmail_token")
    if not creds:
        raise ValueError("Houve um erro na autenticação do GMail API!")

    service = build("gmail", "v1", credentials=creds)
    return service
