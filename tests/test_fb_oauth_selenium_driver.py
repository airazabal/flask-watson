import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from nose.tools import *

class OauthScript(object):
	"""A test Oauth user sign in for Facebook access"""

	def __init__(self):
		#test user from Cerebri AI test Facebook App
		self.fbEmail = str(os.getenv('FB_OAUTH_EMAIL','xmcmlmu_thurnson_1469652579@tfbnw.net'))
		self.fbPassword = str(os.getenv('FB_OAUTH_PASSWORD', 'MarkyMark2016')) 

	def setup(self):
		#open the flask-front-end bluemix server
		self.server = webdriver.Firefox()
		self.server.get('http://flask-front-end.mybluemix.net')
		assert "Cerebri Oauth Tester" in self.server.title

	def run(self):
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

		#checks to see if the window has closed - if the user is new to the app and hasn't authenticated before
		#it will ask them to confirm the set of permissions that Facebook is asking for
		if len(self.server.window_handles) == 2:
			confirm = self.server.find_element(By.NAME, "__CONFIRM__")
			confirm.click()

		#switch back to the main window
		self.server.switch_to_window(self.server.window_handles[0])

		#check the text indicator as to how the POST request to the watson connector went
		checker = self.server.find_element(By.ID, "auth_check")
		assert checker.text == "SUCCESS"

	def teardown(self):
		self.server.close()

def test_ouath_flow():
	main = OauthScript()
	main.setup()
	main.run()
	main.teardown()
