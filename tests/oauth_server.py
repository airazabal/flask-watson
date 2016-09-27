import os
from flask import Flask
from flask import render_template
from flask import request
from twitter import *
import requests

import webbrowser
import time

app = Flask(__name__)

port = int(os.getenv('VCAP_APP_PORT', '5001'))
test_backend_url = os.getenv('TEST_BACKEND_URL')

def parse_oauth_tokens(result):
    for r in result.split('&'):
        k, v = r.split('=')
        if k == 'oauth_token':
            oauth_token = v
        elif k == 'oauth_token_secret':
            oauth_token_secret = v
    return oauth_token, oauth_token_secret

@app.route('/')
def home():
	return 'Hello there friend.  Looks like you might be lost?'

@app.route('/facebook')
def Oauth():
	return render_template('facebook_oauth.html', test_backend_url=test_backend_url)

@app.route('/twitter', methods=['GET', 'POST'])
def twitter():
	if request.method == 'GET':
		twitter = Twitter(
			auth=OAuth('', '', os.getenv('TW_CONSUMER_KEY'), os.getenv('TW_CONSUMER_SECRET')),
			format='', api_version=None)
		
		global req_token 
		global req_token_secret 
		req_token, req_token_secret = parse_oauth_tokens(twitter.oauth.request_token(oauth_callback="oob"))

		oauth_url = ('https://api.twitter.com/oauth/authorize?oauth_token=' + req_token + '&force_login=true')

		return render_template('twitter_oauth.html', oauth_url=oauth_url)
	
	elif request.method == 'POST':
		handle = request.form['handle']
		oauth_verifier = request.form['pin']

		twitter = Twitter(
			auth=OAuth(req_token, req_token_secret, os.getenv('TW_CONSUMER_KEY'), os.getenv('TW_CONSUMER_SECRET')),
			format='', api_version=None)

		oauth_token, oauth_token_secret = parse_oauth_tokens(twitter.oauth.access_token(oauth_verifier=oauth_verifier))

		twitter_be_url = (test_backend_url + '/tw_piroute')

		# POST to the backend
		be = requests.post( twitter_be_url,
			json={"username": handle, "token": oauth_token, "token_key" : oauth_token_secret})

		if be.status_code == 200:
			return render_template('twitter_oauth_complete.html')
		else:
			status_code = be.status_code
			error_message = be.text
			return render_template('twitter_oauth_failed.html', status_code=status_code, error_message=error_message)

	else:
		return "Try a GET request to this route in order to authenticate"

@app.route('/google')
def google():
	return render_template('google_oauth.html', test_backend_url=test_backend_url)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port)