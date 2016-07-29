import os
from flask import Flask
from flask import request
from flask import json
from flask import jsonify
from watsoncaller.personality_insights_wrapper import PersonalityInsight


app = Flask(__name__)

@app.route('/')
def index():
    return 'Server is working try the /pitest route'

@app.route('/test')
def hello():
    return 'Hello, World'

@app.route('/piroute', methods=['GET','POST'])
def PIroute():
    if request.method == 'GET':
        return "Server is running and route is active"
    if request.method == 'POST':
        if request.headers['Content-Type'] == 'application/json':
            validated_json = json_validation(request.json)
            return str(pi_instantiation().return_pi(validated_json))
        else :
            return "Invalid data"

@app.route('/pitest')
def PItest():
    return str(pi_instantiation(mock=True).return_pi('mock data'))

port = int(os.getenv('VCAP_APP_PORT', '5000'))

def json_validation(json_data):
    try:
        request_data = json.loads(json.dumps(json_data))
        payload = request_data['text']
        return payload
    except:
        raise Exception("Bad Data")

def pi_instantiation(mock = False):
    if mock:
        return PersonalityInsight({'MOCK':True, 'username': True,'password': True, 'url': True})
    else:
        try:
            username = os.getenv('PIUsername')
            password = os.getenv('PIPassword')
            url = os.getenv('PIUrl')
            return PersonalityInsight({'username':username,'password':password,'url':url})
        except:
            raise Exception("environment variables dont exist")   

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=port)