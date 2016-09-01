import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nose.tools import *
import time 

class TWOauthScript(object):
	"""A test of the Twitter OAuth flow for access to data for PIs"""

	def __init__(self):
		self.twHandle = str(os.getenv('TW_OAUTH_HANDLE'))
		self.twPassword = str(os.getenv('TW_OAUTH_PASSWORD'))
		self.frontEndUrl = str(os.getenv('TEST_FRONTEND_URL'))
		self.artifact_dir = str(os.getenv('CIRCLE_ARTIFACTS'))

	def setup(self):
		# open the test front end bluemix server, twitter route
		
		# USE FIREFOX TO TEST VISUALLY ON LOCAL MACHINE. PHANTOMJS FOR SERVER TESTS.
		self.server = webdriver.Firefox()
		
		# self.server = webdriver.PhantomJS()

		self.server.get(self.frontEndUrl + "/twitter")
		assert "cerebri-flask-watson" in self.server.title

	def run(self):
		def ensure_dir(pathname):
			d = os.path.dirname(pathname)
			if not os.path.exists(d):
				os.makedirs(d)

		screenshot_dir = (self.artifact_dir + '/screenshots')
		ensure_dir(screenshot_dir)
		print screenshot_dir

		# begin the Oauth flow with the link on twitter_oauth.html
		auth = self.server.find_element(By.NAME, 'start_oauth')
		auth.click()

		# switch to Twitter prompt window that opens up
		self.server.switch_to_window(self.server.window_handles[1])
		assert "Twitter" in self.server.title

		loginUsername = self.server.find_element(By.ID, "username_or_email")
		loginUsername.send_keys(self.twHandle)
		loginPass = self.server.find_element(By.ID, "password")
		loginPass.send_keys(self.twPassword)
		loginSubmit = self.server.find_element(By.ID, "allow")
		loginSubmit.click()

		self.server.save_screenshot(screenshot_dir + '/twitter_pin.png')

		# select the PIN that is provided by the Twitter page
		pin = self.server.find_element(By.XPATH, "/html/body/div[@id='bd']/div[@id='oauth_pin']/p/kbd").text
		
		# switch back to the front end html
		self.server.switch_to_window(self.server.window_handles[0])
		assert "cerebri-flask-watson" in self.server.title
		
		# enter the pin number and the users twitter handle, submit to make a call to the test back end
		pin_entry = self.server.find_element(By.NAME, "pin")
		pin_entry.send_keys(pin)
		handle_entry = self.server.find_element(By.NAME, "handle")
		handle_entry.send_keys(self.twHandle)
		submit = self.server.find_element(By.NAME, "submit_button")
		submit.click()

		# check that the request returned with status code 200
		try:
			assert "authentication complete" in self.server.title
		finally:
			self.server.save_screenshot(screenshot_dir + '/auth_not_complete.png')
			self.server.quit()

	def teardown(self):
		self.server.quit()

def test_tw_oauth():
	main = TWOauthScript()
	main.setup()
	main.run()
	main.teardown()