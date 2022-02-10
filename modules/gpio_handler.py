from modules.sem_tocar_config import *
import RPi.GPIO as GPIO
from time import sleep
import logging
logger = logging.getLogger(__name__)


def problem_found():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RED_LED_PIN, GPIO.OUT, initial=GPIO.LOW)

    GPIO.output(RED_LED_PIN, True)
    
    GPIO.output(BUZZER_PIN, True)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, False)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, True)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, False)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, True)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, False)
    sleep(0.5)
    
    GPIO.output(BUZZER_PIN, True)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, False)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, True)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, False)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, True)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, False)
    sleep(0.5)
    
    GPIO.output(BUZZER_PIN, True)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, False)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, True)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, False)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, True)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, False)
    sleep(0.5)
    
    GPIO.output(RED_LED_PIN, False)
    
    GPIO.cleanup()

def entrance_not_allowed():
    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RED_LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    GPIO.output(RED_LED_PIN, True)
    
    GPIO.output(BUZZER_PIN, True)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, False)
    sleep(0.2)

    GPIO.output(BUZZER_PIN, True)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, False)
    sleep(0.2)
    
    GPIO.output(BUZZER_PIN, True)
    sleep(0.2)
    GPIO.output(BUZZER_PIN, False)
    
    GPIO.output(RED_LED_PIN, False)

    GPIO.cleanup()

def entrance_allowed():

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT, initial=GPIO.LOW)

    GPIO.output(GREEN_LED_PIN, True)    
    GPIO.output(BUZZER_PIN, True)
    sleep(0.5)
    GPIO.output(BUZZER_PIN, False)
    GPIO.output(GREEN_LED_PIN, False)    
   
    GPIO.cleanup()

def qr_found_warn():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BLUE_LED_PIN, GPIO.OUT, initial=GPIO.LOW)

    GPIO.output(BLUE_LED_PIN, True)
    
    GPIO.output(BUZZER_PIN, True)
    sleep(0.1)
    GPIO.output(BUZZER_PIN, False)
    sleep(0.1)

    GPIO.output(BUZZER_PIN, True)
    sleep(0.1)
    GPIO.output(BUZZER_PIN, False)
    
    GPIO.output(BLUE_LED_PIN, False)

    
    GPIO.cleanup()


def unlock():
    GPIO.setmode(GPIO.BOARD)
 
    GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    
    GPIO.output(GREEN_LED_PIN, True)    

    GPIO.output(RELAY_PIN, True)
    
    sleep(OPEN_DOOR)
    
    GPIO.output(RELAY_PIN, False)
    
    GPIO.output(GREEN_LED_PIN, False)    

 
    GPIO.cleanup()
    