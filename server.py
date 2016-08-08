import os
from flask import Flask
from flask import request
from flask import json
from flask import jsonify
from fbcaller.fbOauth import FbOauth as FB
from watsoncaller.personality_insights_wrapper import PersonalityInsight
from helper import json_validation, pi_instantiation, unpack_fb_posts
from errorHandler import ErrorHandler
from flask_cors import CORS

app = Flask(__name__)
port = int(os.getenv('VCAP_APP_PORT', '5000'))

cors = CORS(
    app, resources={r'/*': {"origins": os.getenv('TEST_FRONT_END_URL')}})


@app.errorhandler(ErrorHandler)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


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
            if not request.headers['Content-Type'] == 'application/json':
                raise ErrorHandler('Content type needs to be application/json')
            else:
                vj = json_validation(request.json)
                data = FB(token=vj['oauth_token'], fbid=vj['user_id']).get_fb_data(
                    ['name', 'email', 'posts'])
                data = unpack_fb_posts(data)
                return jsonify(pi_instantiation().return_pi(data))
        except Exception as e:
            raise ErrorHandler(
                str(e), payload={'input': request.json})


@app.route('/pitest')
def PItest():
    return str(pi_instantiation(mock=True).return_pi('mock data'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)