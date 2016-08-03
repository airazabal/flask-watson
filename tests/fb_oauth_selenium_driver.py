from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class OauthScript(object):

	def __init__(self):
		#test user from Cerebri AI test Facebook App
		self.fbEmail = "xmcmlmu_thurnson_1469652579@tfbnw.net"
		self.fbPassword = "MarkyMark2016" 

	def run(self):
		#open the mini-oauth server that will ask the user if they authorize the app
		server = webdriver.Firefox()
		server.get('http://localhost:5001/oauth')
		win1 = server.window_handles
		assert "Cerebri Oauth Tester" in server.title

		auth = server.find_element(By.NAME, "authorize")
		auth.click()

		server.switch_to_window(server.window_handles[1])
		assert "Facebook" in server.title

		loginEmail = server.find_element(By.NAME, "email")
		loginEmail.send_keys(self.fbEmail)
		loginPass = server.find_element(By.NAME, "pass")
		loginPass.send_keys(self.fbPassword)
		loginSubmit = server.find_element(By.NAME, "login")
		loginSubmit.click()

		confirm = server.find_element(By.NAME, "__CONFIRM__")
		confirm.click()

		#server.close()
		#fb.close()

	def checkServer(self):
		pass

main = OauthScript()
main.run()