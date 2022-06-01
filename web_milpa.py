
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import serial
import struct
import time
from threading import Lock

arduino = None
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
    return render_template('index.html', sync_mode=socket_.async_mode)

@socket_.on('openSerial', namespace='/sensor')
def openSerial():
    # Open the serial port to the arduino
    arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
    if arduino.isOpen():
        print("{} connected!".format(arduino.port))
        emit('serialOpen')

@socket_.on('readSensor', namespace='/sensor')
def readSerial():
    if arduino != None:
        incoming = arduino.readline().decode('ascii').strip()
        print("{} incoming".format(incoming))
        if incoming != "":
            print(incoming)
            arduino.flushInput()
            status = float(incoming)
            message = compare(status)
            print('emitting data')
            emit('sensorData', { "data": message })
        else:
            arduino.flushInput()
            print("incoming was empty")

if __name__ == "__main__":
    readSerial()
    socket_.run(app, host='0.0.0.0', debug=True)
