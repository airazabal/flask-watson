import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class OauthScript(object):
	"""A test Oauth user sign in for Facebook access"""

	def __init__(self):
		#test user from Cerebri AI test Facebook App
		self.fbEmail = str(os.environ.get('FB_OAUTH_EMAIL'))
		self.fbPassword = str(os.environ.get('FB_OAUTH_PASSWORD') 

	def setup(self):
		#open the mini-oauth server that will ask the user if they authorize the app and turn off security settings
		self.server = webdriver.Firefox()

		self.server.get('http://localhost:5001/oauth')
		assert "Cerebri Oauth Tester" in self.server.title

	def run(self):
		auth = self.server.find_element(By.NAME, "authorize")
		auth.click()

		self.server.switch_to_window(self.server.window_handles[1])
		assert "Facebook" in self.server.title

		loginEmail = self.server.find_element(By.NAME, "email")
		loginEmail.send_keys(self.fbEmail)
		loginPass = self.server.find_element(By.NAME, "pass")
		loginPass.send_keys(self.fbPassword)
		loginSubmit = self.server.find_element(By.NAME, "login")
		loginSubmit.click()

		if len(self.server.window_handles) == 2:
			confirm = self.server.find_element(By.NAME, "__CONFIRM__")
			confirm.click()

		self.server.switch_to_window(self.server.window_handles[0])

		checker = self.server.find_element(By.ID, "auth_check")
		assert checker.text == "FAILURE"

	def teardown(self):
		self.server.close()

main = OauthScript()
main.setup()
main.run()
#main.teardown()