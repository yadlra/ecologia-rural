# from tkinter import W
from flask import Flask 
import time
import RPi.GPIO as GPIO
from datetime import time

app = Flask(__name__) 

TRIG = 11
ECHO = 10

def setup():
   GPIO.setmode(GPIO.BOARD)
   GPIO.setup(TRIG, GPIO.OUT)
   GPIO.setup(ECHO, GPIO.IN)

def distance():
   GPIO.output(TRIG, 0)
   time.setup(0.000002)

   GPIO.output(TRIG, 1)
   GPIO.sleep(0.00001)
   GPIO.output(TRIG, 0)

   while GPIO.input(ECHO) == 0:
     a = 0
   time1 = time.time()
      
   while GPIO.input(ECHO) == 1:
     a = 1
   time2 = time.time()

   during = time2 - time1
   return during * 340 / 2 * 100


@app.route("/") 
def index(): 
   setup()
   dist = distance()
   dist_round = round(dist)
   
   return render_template("index.html", dist_round = dist_round)
   # "🌱, plants" 

  

if __name__ == '__main__': 
   app.run(port=5000, host='0.0.0.0', debug=True) # application will start listening for web request on port 5000