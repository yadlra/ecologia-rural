from flask import Flask, render_template
from flask_socketio import SocketIO
import datetime
import serial
import struct
import time

async_mode = None
app = Flask(__name__)
socket_ = SocketIO(app, async_mode=async_mode)


def template(title = "HELLO!", text = ""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateDate

def compare(s):
    m = "there was an error"
    if s > -1.0:
        if s < 200:
            m = "200"
        elif s < 300:
            m = "300"
        elif s < 500:
            print(s)
            m = "500"
        elif s < 700:
            print(s)
            m = "700"
        else:
            print(s)
            m = "> 700"
    
    

@app.route("/")
def index():
    # templateData = template()
    # return render_template('main.html', **templateData)
    
    message = "unknown"
    status = -1.0

    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(0.1)
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    val = arduino.readline()
                    print(val)
                    arduino.flushInput()
                    status = struct.unpack('<f', val)
                    message = compare(status)
                    
                    return render_template('index.html',
                           sync_mode=socket_.async_mode)

    

    templateData = template(text = message)
    # return render_template('main.html', **templateData)

    

if __name__ == "__main__":
    socket_.run(app, host='0.0.0.0', debug=True)
   
