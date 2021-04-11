import logging
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)

# If modifying these scopes, delete the file token.pickle.


def authenticate(scope, credentials, token):
    creds = None

    if os.path.exists(token):
        with open(token, "rb") as token_file:
            creds = pickle.load(token_file)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials, scope)
            creds = flow.run_local_server(port=0)

        with open(token, "wb") as token:
            pickle.dump(creds, token)

    return creds


def get_calendar_service():
    """Provides Gcalendar API auth and service
    PT:Lida com autenticação e serviços do Gcalendar API

    Returns:
        Gcalendar API service
    """
    logger.debug('get_calendar_service()')

    if "GCAL_TOKEN_FILE" not in os.environ:
        raise KeyError("Environment variable GCAL_TOKEN_FILE not defined!")
    if "GCAL_CREDENTIALS_FILE" not in os.environ:
        raise KeyError(
            "Environment variable GCAL_CREDENTIALS_FILE not defined!"
        )
    gcal_creds = os.environ["GCAL_CREDENTIALS_FILE"]
    calendar_token = os.environ["GCAL_TOKEN_FILE"]
    creds = authenticate(["https://www.googleapis.com/auth/calendar"], gcal_creds, calendar_token)
    if not creds:
        raise ValueError("There was an unexpected behavior during authentication!")
    service = build("calendar", "v3", credentials=creds)
    return service


def get_gmail_service():
    """Provides Gmail API auth and service  
    PT:Lida com autenticação e serviços do Gmail API
    
    Returns:
        Gmail API service
    """
    logger.debug('get_gmail_service()')

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if "MAIL_TOKEN_FILE" not in os.environ:
        raise KeyError("Environment variable MAIL_TOKEN_FILE not defined!")
    if "MAIL_CREDENTIALS_FILE" not in os.environ:
        raise KeyError(
            "Environment variable MAIL_CREDENTIALS_FILE not defined!"
        )
    mail_creds = os.environ["MAIL_CREDENTIALS_FILE"]
    mail_token = os.environ["MAIL_TOKEN_FILE"]
    creds = authenticate(["https://www.googleapis.com/auth/gmail.send"], gcal_creds, calendar_token)
    if not creds:
        raise ValueError("There was an unexpected behavior during authentication!")

    service = build("gmail", "v1", credentials=creds)
    return service
