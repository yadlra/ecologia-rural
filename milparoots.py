from flask import Flask # include the flask library 

app = Flask(__name__) 

@app.route("/") 
def index(): 
   return "🌱, plants" 
  

if __name__ == '__main__': 
   app.run(port=5000, host='0.0.0.0', debug=True) # application will start listening for web request on port 5000
