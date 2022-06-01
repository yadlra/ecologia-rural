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
    

@app.route("/")
def hello():
    templateData = template()
    # return render_template('main.html', **templateData)
    return render_template('index.html',
                           sync_mode=socket_.async_mode)


@app.route("/sensor")
def action():
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
            except:
                status = -1.0

    if status > -1.0:
        if status < 200:
            message = "200"
        elif status < 300:
            message = "300"
        elif status < 500:
            print(status)
            message = "500"
        elif status < 700:
            print(status)
            message = "700"
        else:
            print(status)
            message = "> 700"
    else:
        message = "There was an error"

    templateData = template(text = message)
    # return render_template('main.html', **templateData)
    return render_template('index.html',
                           sync_mode=socket_.async_mode)

if __name__ == "__main__":
    socket_.run(app, debug=True)
    app.run(port=5000, host='0.0.0.0', debug=True)
