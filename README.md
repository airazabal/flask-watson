# falcon-watson
This is service for scraping fb posts and analyzing it using watson PI.

The readme will change soon.

###Instructions to run
copy env_var_example.sh to env_var and fill out credentials.

run
`python hello.py`




###Instructions to test the google auth
0) open 2 terminal windows
1) load the required environment vars (PIUsername, PIPassword, and PIUrl)
2) navigate in window 1 to the tests directory
	activate the virtual environment and then run the server with gunicorn
	$ source env/bin/activate
	$ export TEST_BACKEND_URL=http://localhost:5000
	$ gunicorn oauth_server:app 
3) in window 2 load the virtual environment and start the server for the main web app
	$ source env/bin/activate
	$ python server.py  
4) In the web browser, open localhost:8080/google
5) open the inspector in chrome/safari (if you use any other browser, shame on you)
5) Follow through on the signin with google plus
6) look in the network tab for the call made to google_auth_pi and examine the response to validate that you are gettin a message from IBM watson. 


