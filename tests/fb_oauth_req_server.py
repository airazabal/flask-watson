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

def parse_oauth_tokens(result):
    for r in result.split('&'):
        k, v = r.split('=')
        if k == 'oauth_token':
            oauth_token = v
        elif k == 'oauth_token_secret':
            oauth_token_secret = v
    return oauth_token, oauth_token_secret

@app.route('/oauth')
def Oauth():
	return render_template('test_oauth.html')

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

		try:
			r = webbrowser.open(oauth_url)
			time.sleep(2)

			if not r:
				raise Exception()
		except:
			return "Could not open authentication window"
		return render_template('twitter_oauth.html')
	
	elif request.method == 'POST':
		handle = request.form['handle']
		oauth_verifier = request.form['pin']

		twitter = Twitter(
			auth=OAuth(req_token, req_token_secret, os.getenv('TW_CONSUMER_KEY'), os.getenv('TW_CONSUMER_SECRET')),
			format='', api_version=None)

		oauth_token, oauth_token_secret = parse_oauth_tokens(twitter.oauth.access_token(oauth_verifier=oauth_verifier))

		# POST to the backend
		be = requests.post('https://twitter-watson-dev.mybluemix.net/tw_piroute',
			json={"username": handle, "token": oauth_token, "token_key" : oauth_token_secret})

		print be.text
		return render_template('twitter_oauth_complete.html')

	else:
		return "Try a GET request to this route in order to authenticate"

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port)