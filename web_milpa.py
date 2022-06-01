from flask import Flask, render_template
import datetime
import water


app = Flask(__name__)

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
    return render_template('main.html', **templateData)


@app.route("/sensor")
def action():
    status = water.get_status()
    message = status
    # if (status == 1):
    #     # message = "Water me please!"
    # else:
    #     # message = "I'm a happy plant"

    templateData = template(text = message)
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0', debug=True)
