import os
from flask import Flask
from flask import render_template

app = Flask(__name__)

port = int(os.getenv('VCAP_APP_PORT', '5001'))

@app.route('/oauth')
def Oauth():
	return render_template('test_oauth.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port)