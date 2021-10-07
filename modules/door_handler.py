from modules.sem_tocar_config import *
import RPi.GPIO as GPIO
from time import sleep


def unlock():
    GPIO.setmode(GPIO.BOARD)
    mode = GPIO.getmode()
 
    GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    GPIO.output(RELAY_PIN, True)
    #print(GPIO.input(8))
    
    sleep(OPEN_DOOR)
    
    GPIO.output(RELAY_PIN, False)
    #print(GPIO.input(8))    
    
    GPIO.cleanup()