from modules.sem_tocar_config import *
from gpiozero import OutputDevice
import time


def unlock():
    maglock = OutputDevice(2, initial_value=False)
    maglock.on()
    print("MAGLOCK ON")
    time.sleep(5)
    maglock.off()
    print("MAGLOCK OFF")

    
    