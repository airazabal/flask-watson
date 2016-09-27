import os
import requests
from flask import Flask
from flask import request
from flask import json
from flask import jsonify
from fbcaller.fbOauth import FbOauth as FB
from watsoncaller.personality_insights_wrapper import PersonalityInsight
from googlecaller.google_plus_wrapper import getUserData, getUserCommentsAsString
from helper import json_validation, pi_instantiation, unpack_fb_posts, unpack_tweets, check_fields
from errors import ErrorHandler
from flask_cors import CORS
from twitter import *

app = Flask(__name__)
port = int(os.getenv('VCAP_APP_PORT', '5000'))

cors = CORS(
	app, resources={r'/*': {"origins": os.getenv('TEST_FRONT_END_URL', '*')}})

@app.errorhandler(ErrorHandler)
def handle_invalid_usage(error):
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.route('/')
def index():
	return 'Server is working try the /facebook, /google or /twitter routes'

@app.route('/test')
def hello():
	return 'Hello, World'

@app.route('/fb_piroute', methods=['GET', 'POST'])
def PIroute_facebook():
	if request.method == 'GET':
		return "Server is running and Facebook route is active"
	if request.method == 'POST':
		try:
			needed = ['oauth_token', 'user_id']
			check_fields(needed, request.json)
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

@app.route('/tw_piroute', methods=['GET', 'POST'])
def PIroute_twitter():
	if request.method == 'GET':
		return "Server is running and the Twitter route is active"
	if request.method == 'POST':
		try:
			needed = ['username', 'token', 'token_key']
			check_fields(needed, request.json)
			if not request.headers['Content-Type'] == 'application/json':
				return request.headers['Content-Type']
			else:
				valid_tw = json_validation(request.json)
				handle = valid_tw['username']
				token = valid_tw['token']
				token_secret = valid_tw['token_key']
				con_secret = os.getenv('TW_CONSUMER_SECRET')
				con_key = os.getenv('TW_CONSUMER_KEY')
				t = Twitter(auth=OAuth(token, token_secret, con_key, con_secret))
				data = unpack_tweets(t.statuses.user_timeline(screen_name=handle))
				return jsonify(pi_instantiation().return_pi(data))
		except Exception as e:
			raise ErrorHandler(str(e), payload={'input': request.json})

@app.route('/gp_piroute', methods=['GET', 'POST'])
def PIroute_google():
    if request.method == 'GET':
        return "Server is running and the Google Plus route is active"
    if request.method == 'POST':
        try:
        	needed = ['access_token']
        	check_fields(needed, request.json)
        	if not request.headers['Content-Type'] == 'application/json':
        		raise ErrorHandler('Content type needs to be application/json')
        	else:
        		token = json_validation(request.json)['access_token']
        		data = getUserCommentsAsString(getUserData(token))
        		return jsonify(pi_instantiation().return_pi(data))
        except Exception as e:
        		raise ErrorHandler(str(e), payload={'input': request.json})

@app.route('/pitest')
def PItest():
	return str(pi_instantiation(mock=True).return_pi('mock data'))


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port)
