from selenium import webdriver

#initialize two browser windows, one for facebook and one for the ouath server
fb = webdriver.Firefox()
oauth = webdriver.Firefox()

fb.get('https://en-gb.facebook.com/login/')
oauth.get('http://google.ca/')

