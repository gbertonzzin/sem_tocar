import logging
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from modules.sem_tocar_config import *
#from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)

#if "GOOGLE_CREDENTIALS_FILE" not in os.environ:
#    raise KeyError("Environment variable GOOGLE_CREDENTIALS_FILE not defined!")
#GOOGLE_CREDS = os.environ["GOOGLE_CREDENTIALS_FILE"]


def authenticate(scope, token):
    logger.debug("authenticate()")
    creds = None

    if os.path.exists(token):
        try:
            with open(token, "rb") as token_file:
                creds = pickle.load(token_file)   
                #logger.info(f"Utilizando o token {token} para o escopo {scope}...") 
        except:
            logger.warning(f'Não foi possível carregar o token {token}!')    

    if not creds or not creds.valid:
        logger.warning("Credenciais inválidas or expiradas!")
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                logger.warning('Ocorreu um erro ao tentar renovar as credenciais!')
        else:
            logger.info("Solicitando acesso ao usuário...")
            if os.path.exists(GOOGLE_CREDS):
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDS, scope)
                    creds = flow.run_local_server(port=0)   #FIX: If user closes the auth browser window, everything freezes
                                                            #maybe add a timer?
                except:
                    logger.warning('Ocorreu um erro ao solicitar acesso ao usuário!')
            else:
                logger.warning(f"Arquivo de credenciais {GOOGLE_CREDS} não encontrado!")
                return False
        try:
            with open(token, "wb") as token_file:
                logger.info(f"Criando token de acesso '{token}.json' para o escopo '{scope}'.")
                pickle.dump(creds, token_file)
        except:
            logger.warning(f"Ocorreu um erro ao criar o token '{token}.json' para o escopo '{scope}'!")

    return creds


def get_service(scope):
    
    logger.debug("get_service()")
    
    if scope == 'gcal':
        logger.debug("get_calendar_service()")
        creds = authenticate(["https://www.googleapis.com/auth/calendar"], "gcal_token")
        if not creds:
            raise ValueError("Houve um erro na autenticação do GCal API!")
        service = build("calendar", "v3", credentials=creds)
        return service
    
    elif scope == 'gmail':
        logger.debug("get_gmail_service()")
        creds = authenticate(["https://www.googleapis.com/auth/gmail.send"], "gmail_token")
        if not creds:
            raise ValueError("Houve um erro na autenticação do GMail API!")

        service = build("gmail", "v1", credentials=creds)
        return service
    else:
        raise ValueError('Escopo inválido!')

