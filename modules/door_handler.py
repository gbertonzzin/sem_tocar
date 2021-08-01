from modules.sem_tocar_config import *
import RPi.GPIO as GPIO
import time


def unlock():
    GPIO.setmode(GPIO.BOARD)
    mode = GPIO.getmode()
    print(mode)
    GPIO.setup(16, GPIO.OUT, initial=GPIO.LOW)
    
    GPIO.output(16, True)
    print(GPIO.input(16))
    
    time.sleep(3)
    
    GPIO.output(16, False)
    print(GPIO.input(16))    
    
    GPIO.cleanup()