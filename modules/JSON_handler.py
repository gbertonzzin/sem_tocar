"""Handles JSON files
PT:Lida com arquivos JSON
"""
import logging
import os, json

logger = logging.getLogger(__name__)


def json_file_check(new_json, last_json):
    """Checks if the necessary database files exist
    PT:Verifica se os arquivos de database necessários existem

    Args:
    new_json: Filename for the requested events
    last_json: Filename for the previous requested events

    Returns:
    Boolean
    """
    logger.debug("json_file_check()" )

    if os.path.isfile(new_json):
        logger.info(f"{new_json} existe! \n    Prosseguindo...")
        if os.path.isfile(last_json):
            logger.info(f"{last_json} existe! \n    Prosseguindo...")
            os.remove(last_json)
            os.rename(new_json, last_json)
            logger.info(f"{new_json} foi renomeado para {last_json}")
            return True
        else:
            logger.warning(f"{last_json} não encontrado!")
            os.rename(new_json, last_json)
            logger.info(f"{new_json} foi renomeado para {last_json}")
            return True
    else:
        no_new_json = f"{new_json} não encontrado"
        logger.warning(no_new_json)
        return no_new_json


def compare_json(new_json, last_json):
    """Compares the json files to check for new events  PT:

    Args:
        new_json: Filename for the requested events
        last_json: Filename for the previous requested events
    Returns:
        A set with all new events IDs, or False
    """
    logger.debug("compare_json()")
    
    with open(new_json) as f:
        present_data = json.load(f)
    with open(last_json) as f:
        last_data = json.load(f)

    present_events = set([present_data[event]["id"] for event in present_data])
    last_events = set([last_data[event]["id"] for event in last_data])
    new_events = list(present_events.difference(last_events))

    if len(new_events) > 0:
        logger.info(f"Novos eventos: {new_events}")
    else:
        logger.info("Não há novos eventos!")
    return new_events
