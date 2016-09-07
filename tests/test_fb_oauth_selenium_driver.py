import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nose.tools import *
import time 

class FBOauthScript(object):
	"""A test of the Facebook OAuth flow for access to data for PIs"""

	def __init__(self):
		# test user from Cerebri AI test Facebook App
		self.fbEmail = str(os.getenv('FB_OAUTH_EMAIL'))
		self.fbPassword = str(os.getenv('FB_OAUTH_PASSWORD'))
		self.frontEndUrl = str(os.getenv('TEST_FRONTEND_URL'))
		self.screenshotDir = (str(os.getenv('CIRCLE_ARTIFACTS')) + '/screenshots/facebook/')

		if not os.path.exists(self.screenshotDir):
			os.makedirs(self.screenshotDir)

	def setup(self):
		# open the flask-front-end bluemix server
		self.server = webdriver.PhantomJS()
		self.wait = WebDriverWait(self.server, 10)
		self.server.get(self.frontEndUrl + '/facebook')
		try:
			assert "Cerebri Oauth Tester" in self.server.title
		except:
			self.server.save_screenshot(self.screenshotDir + '/no_start_page.png')
			self.server.quit()
			raise

	def run(self):
		# click the 'Authorize!' button
		try:
			auth = self.server.find_element(By.NAME, "authorize")
			auth.click()
		except:
			self.server.save_screenshot(self.screenshotDir + '/no_login_button.png')
			self.server.quit()
			raise

		# switch to the popup window that asks for a Facebook login
		self.server.switch_to_window(self.server.window_handles[1])
		try:
			assert "Facebook" in self.server.title
		except:
			self.server.save_screenshot(self.screenshotDir + '/no_login_page.png')
			self.server.quit()
			raise			

		# enter Facebook credentials and hit the login button
		try:
			loginEmail = self.server.find_element(By.NAME, "email")
			loginEmail.send_keys(self.fbEmail)
			loginPass = self.server.find_element(By.NAME, "pass")
			loginPass.send_keys(self.fbPassword)
			loginSubmit = self.server.find_element(By.NAME, "login")
			loginSubmit.click()
		except:
			self.server.save_screenshot(self.screenshotDir + '/login_problem.png')
			self.server.quit()
			raise			

		# switch back to the main window
		self.server.switch_to_window(self.server.window_handles[0])
		time.sleep(2)

		# check that the POST request returned with status code 200 from watson connector
		checker = self.server.find_element(By.ID, "auth_check")
		print checker.text, 'Checker text'

		try:
			assert checker.text == "SUCCESS"
		except:
			self.server.save_screenshot(self.screenshotDir + '/auth_failed.png')
			self.server.switch_to_window(self.server.window_handles[1])
			self.server.save_screenshot(self.screenshotDir + '/auth_failed_2.png')
			self.server.quit()
			raise			

	def teardown(self):
		self.server.quit()

def test_fb_flow():
	main = FBOauthScript()
	main.setup()
	main.run()
	main.teardown()
