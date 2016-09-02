import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from nose.tools import *
import time 

class GPOauthScript(object):
	"""A test of the Google+ OAuth flow for access to data for PIs"""

	def __init__(self):
		# test user created for Google+ use
		self.gEmail = str(os.getenv('G_EMAIL'))
		self.gPW = str(os.getenv('G_PW'))

	def setup(self):
		self.server = webdriver.Firefox()
		self.server.get('http://flask-front-end.mybluemix.net/google')

	def run(self):
		#click the 'Authorize!' button
		auth = self.server.find_element(By.ID, "gConnect")
		auth.click()

		#switch to the popup window that asks for a Facebook login
		self.server.switch_to_window(self.server.window_handles[1])
		assert "Sign in - Google Accounts" in self.server.title

		#enter Facebook credentials and hit the login button
		loginEmail = self.server.find_element(By.NAME, "Email")
		loginEmail.send_keys(self.gEmail)
		clickCont = self.server.find_element(By.NAME, 'signIn')
		clickCont.click()

		loginPass = self.server.find_element(By.NAME, "Passwd")
		loginPass.send_keys(self.gPW)
		loginSubmit = self.server.find_element(By.NAME, "signIn")
		loginSubmit.click()

		#switch back to the main window
		self.server.switch_to_window(self.server.window_handles[0])
		time.sleep(5)
		#check the text indicator as to how the POST request to the watson connector went
		checker = self.server.find_element(By.ID, "status")
		print checker.text, 'Checker text'
		assert checker.text == "SUCCESS"

	def teardown(self):
		self.server.close()