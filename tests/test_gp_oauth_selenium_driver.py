import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nose.tools import *
import time 

class GPOauthScript(object):
	"""A test of the Google+ OAuth flow for access to data for PIs"""

	def __init__(self):
		# test user created for Google+ use
		self.gEmail = str(os.getenv('G_EMAIL'))
		self.gPW = str(os.getenv('G_PW'))
		self.frontEndUrl = str(os.getenv('TEST_FRONTEND_URL'))
		self.screenshotDir = (str(os.getenv('CIRCLE_ARTIFACTS')) + '/screenshots/')

		if not os.path.exists(self.screenshotDir):
			os.makedirs(self.screenshotDir)

	def setup(self):
		self.server = webdriver.Firefox()
		self.wait = WebDriverWait(self.server, 10)
		self.server.get(self.frontEndUrl + '/google')
		try:
			assert "Google" in self.server.title
		except:
			self.server.save_screenshot(self.screenshotDir + '/no_start_page.png')
			raise

	def run(self):
		

		#click the 'Authorize!' button
		try:
			
			button = self.wait.until(EC.element_to_be_clickable((By.ID, "signin-button")))
			auth = self.server.find_element(By.XPATH, "/html/body/div[@id='gConnect']/div[@id='signin-button']/div[@class='abcRioButton abcRioButtonWhite']/div[@class='abcRioButtonContentWrapper']")
		except:
			self.server.save_screenshot(self.screenshotDir + '/no_login_button.png')
			self.server.quit()
			raise

		actions = ActionChains(self.server)
		actions.move_to_element(auth).click().perform()

		#switch to the popup window that asks for a Google login
		try:
			self.server.switch_to_window(self.server.window_handles[1])
			assert "Sign in - Google Accounts" in self.server.title
		except:
			self.server.save_screenshot(self.screenshotDir + '/no_login_page.png')
			self.server.quit()
			raise

		#enter Google credentials and hit the login button
		try:
			loginEmail = self.server.find_element(By.NAME, "Email")
			loginEmail.send_keys(self.gEmail)
			clickCont = self.server.find_element(By.NAME, 'signIn')
			clickCont.click()

			loginPass = self.wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
			loginPass.send_keys(self.gPW)
			loginSubmit = self.wait.until(EC.presence_of_element_located((By.XPATH, "//form[@id='gaia_loginform']/div[2]/div/input")))
			loginSubmit.click()
		except:
			self.server.save_screenshot(self.screenshotDir + '/login_problem.png')
			# self.server.quit()
			raise

		#switch back to the main window
		self.server.switch_to_window(self.server.window_handles[0])
		time.sleep(5)
		#check the text indicator as to how the POST request to the watson connector went
		checker = self.server.find_element(By.ID, "status")
		print checker.text, 'Checker text'
		
		try:
			assert checker.text == "SUCCESS"
		except:
			self.server.save_screenshot(self.screenshotDir + '/gp_auth_failed.png')
			self.server.quit()
			raise

	def teardown(self):
		self.server.quit()

def test_gp_oauth():
	main = GPOauthScript()
	main.setup()
	main.run()
	main.teardown()