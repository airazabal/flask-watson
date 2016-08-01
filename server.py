import os
from flask import Flask
from flask import request
from flask import json
from flask import jsonify
from fbcaller.fbOauth import FbOauth as FB
from watsoncaller.personality_insights_wrapper import PersonalityInsight
from helper import json_validation, pi_instantiation

app = Flask(__name__)
port = int(os.getenv('VCAP_APP_PORT', '5000'))


@app.route('/')
def index():
    return 'Server is working try the /pitest route'


@app.route('/test')
def hello():
    return 'Hello, World'


@app.route('/piroute', methods=['GET', 'POST'])
def PIroute():
    if request.method == 'GET':
        return "Server is running and route is active"
    if request.method == 'POST':
        try:
            if request.headers['Content-Type'] == 'application/json':
                vj = json_validation(request.json)
                return jsonify(json.loads(FB(token=vj['oauth_token'], fbid=vj[
                               'user_id']).get_fb_data(['name', 'email', 'posts'])))
            else:
                return "Invalid data"
        except Exception, e:
            return str(e)


@app.route('/pitest')
def PItest():
    return str(pi_instantiation(mock=True).return_pi('mock data'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
