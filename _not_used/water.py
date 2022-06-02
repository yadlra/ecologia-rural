import RPi.GPIO as GPIO
import datetime
import time

init = False

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

# def get_last_watered():
#     try:
#         f = open("last_watered.txt", "r")
#         return f.readline()
#     except:
#         return "NEVER!"
      
def get_status(pin = 5):
    GPIO.setup(pin, GPIO.IN) 
    return GPIO.input(pin)

# def init_output(pin):
#     GPIO.setup(pin, GPIO.OUT)
#     GPIO.output(pin, GPIO.LOW)
#     GPIO.output(pin, GPIO.HIGH)


