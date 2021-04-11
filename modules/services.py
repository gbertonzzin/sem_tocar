import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.pickle.


def get_calendar_service():
    """Provides Gcalendar API auth and service
    PT:Lida com autenticação e serviços do Gcalendar API

    Returns:
        Gcalendar API service
    """
    # print('get_calendar_service()')

    creds = None
    scope = ["https://www.googleapis.com/auth/calendar"]

    if "GCAL_TOKEN_FILE" not in os.environ:
        raise KeyError("Environment variable GCAL_TOKEN_FILE not defined!")

    calendar_token = os.environ["GCAL_TOKEN_FILE"]

    if os.path.exists(calendar_token):
        with open(calendar_token, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if "GCAL_CREDENTIALS_FILE" not in os.environ:
                raise KeyError(
                    "Environment variable GCAL_CREDENTIALS_FILE not defined!"
                )
            gcal_creds = os.environ["GCAL_CREDENTIALS_FILE"]
            flow = InstalledAppFlow.from_client_secrets_file(gcal_creds, scope)
            creds = flow.run_local_server(port=0)

        with open(calendar_token, "wb") as token:
            pickle.dump(creds, token)

    service = build("calendar", "v3", credentials=creds)
    return service


def get_gmail_service():
    """Provides Gmail API auth and service  
    PT:Lida com autenticação e serviços do Gmail API
    
    Returns:
        Gmail API service
    """
    # print('get_gmail_service()')

    creds = None
    scope = ["https://www.googleapis.com/auth/gmail.send"]
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if "MAIL_TOKEN_FILE" not in os.environ:
        raise KeyError("Environment variable MAIL_TOKEN_FILE not defined!")

    mail_token = os.environ["MAIL_TOKEN_FILE"]

    if os.path.exists(mail_token):
        with open(mail_token, "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if "MAIL_CREDENTIALS_FILE" not in os.environ:
                raise KeyError(
                    "Environment variable MAIL_CREDENTIALS_FILE not defined!"
                )
            mail_creds = os.environ["MAIL_CREDENTIALS_FILE"]
            flow = InstalledAppFlow.from_client_secrets_file(mail_creds, scope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(mail_token, "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service
