import os
from flask import Flask
from flask import render_template
from flask import request
import requests

app = Flask(__name__)

port = int(os.getenv('VCAP_APP_PORT', '5001'))

@app.route('/oauth')
def Oauth():
	test_backend_url = os.getenv('TEST_BACKEND_URL')

	return render_template('facebook_oauth.html', test_backend_url=test_backend_url)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port)