import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def Hello():
	return 'This is test'

#port = os.getenv('PORT', '8080')
port = int(os.getenv('VCAP_APP_PORT', '5000'))

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=port)
