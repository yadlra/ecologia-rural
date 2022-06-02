
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import serial
import struct
import time
from threading import Lock

async_mode = None
app = Flask(__name__)
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

def template(title="HELLO!", text="Waiting for data..."):
    templateDate = {
        'title' : title,
        'text' : text
    }
    return templateDate

def compare(s):
    print(s)
    m = "https://blank.com"
    if s > -1.0:
        if s < 200:
            m = "https://www.google.com/"
        elif s < 300:
            m = "https://www.twitter.com"
        elif s < 500:
            m = "https://chootka.com"
        elif s < 700:
            m = "https://weise7.org"
        else:
            m = "https://conrad.de"
    return m

@app.route("/")
def index():
    return render_template('index.html', sync_mode=socket_.async_mode)

@socket_.on('openSerial', namespace='/sensor')
def openSerial():
    # Open the serial port to the arduino
    session["arduino"] = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
    if session["arduino"].isOpen():
        print("{} connected!".format(session["arduino"].port))
        emit('serialOpen')

@socket_.on('readSensor', namespace='/sensor')
def readSerial():
    if session.get("arduino"):
        port = session["arduino"]
        incoming = port.readline().decode('ascii').strip()
        print("{} incoming".format(incoming))
        if incoming != "":
            print(incoming)
            port.flushInput()
            status = float(incoming)
            message = compare(status)
            emit('sensorData', { "data": message })
        else:
            port.flushInput()
            print("incoming was empty")

if __name__ == "__main__":
    socket_.run(app, host='0.0.0.0', debug=True)
