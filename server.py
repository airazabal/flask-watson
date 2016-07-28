import os
from flask import Flask
from flask import request
from flask import json
from flask import jsonify
from personality_insights_wrapper import PersonalityInsightCaller

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
            try:
                request_data = json.loads(json.dumps(request.json))
                payload = request_data['text']
            except:
                return "Bad Data"
            try:
                print "post works"        
                username = os.getenv('PIUsername')
                print username
                password = os.getenv('PIPassword')
                url = os.getenv('PIUrl')
            except:
                print "shit"
                return "environment variables dont exist"
            creds = {'username':username,'password':password,'url':url}
            PIDemo = PersonalityInsightCaller(creds)
            PIDemo.insert_text(payload)
            insights = PIDemo.get_personality()
            return str(insights)
        else :
            return "Invalid data"


@app.route('/pitest')
def PItest():
    print "entered pitest"
    username = 'MOCK'
    password = 'MOCK'
    url = 'MOCK'
    creds = {'username':username,'password':password,'url':url}
    PIDemo = PersonalityInsightCaller(creds)
    PIDemo.insert_text('Random text for the mock code.')
    insights = PIDemo.get_personality()
    return str(insights)

port = int(os.getenv('VCAP_APP_PORT', '5000'))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=port)