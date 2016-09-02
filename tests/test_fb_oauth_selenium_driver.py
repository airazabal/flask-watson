import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from nose.tools import *
import time 


class OauthScript(object):
	"""A test Oauth user sign in for Facebook access"""

	def __init__(self):
		#test user from Cerebri AI test Facebook App
		self.fbEmail = str(os.getenv('FB_OAUTH_EMAIL'))
		self.fbPassword = str(os.getenv('FB_OAUTH_PASSWORD')) 

	def setupFB(self):
		#open the flask-front-end bluemix server
		self.server = webdriver.PhantomJS() 
		self.server.get('http://flask-front-end.mybluemix.net/oauth')
		assert "Cerebri Oauth Tester" in self.server.title

	def runFB(self):
		#click the 'Authorize!' button
		auth = self.server.find_element(By.NAME, "authorize")
		auth.click()

		#switch to the popup window that asks for a Facebook login
		self.server.switch_to_window(self.server.window_handles[1])
		assert "Facebook" in self.server.title

		#enter Facebook credentials and hit the login button
		loginEmail = self.server.find_element(By.NAME, "email")
		loginEmail.send_keys(self.fbEmail)
		loginPass = self.server.find_element(By.NAME, "pass")
		loginPass.send_keys(self.fbPassword)
		loginSubmit = self.server.find_element(By.NAME, "login")
		loginSubmit.click()

		#switch back to the main window
		self.server.switch_to_window(self.server.window_handles[0])
		time.sleep(5)
		#check the text indicator as to how the POST request to the watson connector went
		checker = self.server.find_element(By.ID, "auth_check")
		print checker.text, 'Checker text'
		assert checker.text == "SUCCESS"

	def teardown(self):
		self.server.close()

def test_ouath_flow():
	main = OauthScript()
	main.setupFB()
	main.runFB()
	main.teardown()
