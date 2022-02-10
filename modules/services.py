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
        except:
            logger.warning(f'Não foi possível carregar o token!')    

    if not creds or not creds.valid:
        logger.warning("Credenciais inválidas or expiradas!")
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                logger.warning('Ocorreu um erro ao tentar renovar as credenciais!')
        else:
            if os.path.exists(GOOGLE_CREDS):
                logger.info("Solicitando acesso ao usuário...")
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDS, scope)
                    creds = flow.run_local_server(port=0)   #FIX: If user closes the auth browser window, everything freezes
                                                            #maybe add a timer?
                except Exception as e:
                    logger.warning('Ocorreu um erro ao solicitar acesso ao usuário!')
                    print(e)
            else:
                logger.warning(f"Arquivo de credenciais {GOOGLE_CREDS} não encontrado!")
                return False
        try:
            with open(token, "wb") as token_file:
                logger.info(f"Criando token de acesso.")
                pickle.dump(creds, token_file)
        except Exception as e:
            logger.warning(f"Ocorreu um erro ao criar o token!")
            logger.warning(e)

    return creds


def get_service(scope):
    
    logger.debug("get_service()")
    
    try:
        creds = authenticate([f"https://www.googleapis.com/auth/{scope}"], f"{scope}_token")
        if not creds:
            raise ValueError("Houve um erro na autenticação do {scope} API!")
        service = build(scope if scope == 'calendar' else 'gmail', 'v3' if scope == 'calendar' else 'v1', credentials=creds)
        return service
    except Exception as e:
        logger.warning("Houve um erro ao requisitar o servico!")
        logger.warning(e)