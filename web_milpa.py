from flask import Flask, render_template
from flask_socketio import SocketIO
import serial
import struct
import time
from threading import Lock

async_mode = None
app = Flask(__name__)
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
message = "Waiting for data"
status = -1.0

def template(title="HELLO!", text=""):
    templateDate = {
        'title' : title,
        'text' : text
    }
    return templateDate

def compare(s):
    print(s)
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
    return m

@app.route("/")
def index():
    # templateData = template(text = message)
    # return render_template('main.html', **templateData)
    return render_template('index.html', sync_mode=socket_.async_mode)

@socket_.on('readSensor', namespace='/sensor')
def readSerial():
    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(0.1)
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            val = arduino.readline()
            print(val)
            arduino.flushInput()
            status = struct.unpack('<f', val)
            message = compare(status)
            emit('sensorData', { data: message })

if __name__ == "__main__":
    readSerial()
    socket_.run(app, host='0.0.0.0', debug=True)