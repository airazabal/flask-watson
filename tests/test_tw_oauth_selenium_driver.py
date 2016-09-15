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
		self.screenshotDir = (str(os.getenv('CIRCLE_ARTIFACTS')) + '/screenshots/twitter/')

		if not os.path.exists(self.screenshotDir):
			os.makedirs(self.screenshotDir)

	def setup(self):
		# open the test front end bluemix server, twitter route
		self.server = webdriver.Firefox()
		self.wait = WebDriverWait(self.server, 10)
		self.server.get(self.frontEndUrl + "/twitter")
		try:
			assert "cerebri-flask-watson" in self.server.title
		except:
			self.server.save_screenshot(self.screenshotDir + '/no_start_page.png')
			self.server.quit()
			raise

	def run(self):
		# begin the Twitter Oauth flow with the link on twitter_oauth.html
		try:
			auth = self.server.find_element(By.NAME, 'start_oauth')
			auth.click()
		except:
			self.server.save_screenshot(self.screenshotDir + '/no_login_button.png')
			self.server.quit()
			raise			

		# switch to Twitter prompt window that opens up
		self.server.switch_to_window(self.server.window_handles[1])
		try:
			assert "Twitter" in self.server.title
		except:
			self.server.save_screenshot(self.screenshotDir + '/no_login_page.png')
			self.server.quit()
			raise				

		# enter twitter credentials into twitter page
		try:
			loginUsername = self.server.find_element(By.ID, "username_or_email")
			loginUsername.send_keys(self.twHandle)
			loginPass = self.server.find_element(By.ID, "password")
			loginPass.send_keys(self.twPassword)
			loginSubmit = self.server.find_element(By.ID, "allow")
			loginSubmit.click()
		except:
			self.server.save_screenshot(self.screenshotDir + '/login_problem.png')
			self.server.quit()
			raise

		# select the PIN that is provided by the Twitter page
		try:
			pin = self.server.find_element(By.XPATH, "/html/body/div[@id='bd']/div[@id='oauth_pin']/p/kbd").text
		except:
			self.server.save_screenshot(self.screenshotDir + '/no_pin.png')
			self.server.quit()
			raise			

		# switch back to the front end html
		self.server.switch_to_window(self.server.window_handles[0])
		try:
			assert "cerebri-flask-watson" in self.server.title
		except:
			self.server.save_screenshot(self.screenshotDir + '/no_switchback.png')
			self.server.quit()
			raise			
		
		# enter the pin number and the users twitter handle, submit to make a call to the test back end
		try:
			pin_entry = self.server.find_element(By.NAME, "pin")
			pin_entry.send_keys(pin)
			handle_entry = self.server.find_element(By.NAME, "handle")
			handle_entry.send_keys(self.twHandle)
			submit = self.server.find_element(By.NAME, "submit_button")
			submit.click()
		except:
			self.server.save_screenshot(self.screenshotDir + '/pin_entry_failed.png')
			self.server.quit()
			raise			

		# check that the POST request returned with status code 200 from watson connector
		try:
			assert "authentication complete" in self.server.title
		except:
			self.server.save_screenshot(self.screenshotDir + '/auth_not_complete.png')
			self.server.quit()
			raise

	def teardown(self):
		self.server.quit()

def test_tw_oauth():
	main = TWOauthScript()
	main.setup()
	main.run()
	main.teardown()