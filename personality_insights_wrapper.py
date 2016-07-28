import requests
import json
import csv
import pickle
import urllib
import urllib

class MockPersonalityInsight:

    def return_pi(self, text=None):
        file = open("insights.pickle","rb")
        object_file = pickle.load(file)
        file.close()
        return object_file

class PersonalityInsight(object):

    def __new__(cls, credentials={}):
        check_values = ['username', 'password', 'url']
        if all(value in credentials.keys() for value in check_values) : 
            if 'MOCK' in credentials.values():
                return MockPersonalityInsight()
            else:
                return super(PersonalityInsight, cls).__new__(cls, credentials)    
        else :
            raise ValueError('Illegal Argument Exception')

    def __init__(self, credentials):
        self.username = credentials['username']
        self.password = credentials['password']
        self.url = credentials['url']

    def return_pi(self, text):
        try:
            return json.loads(requests.post(self.url + "/v2/profile",
                                      auth=(self.username, self.password),
                                      headers={"content-type": "text/plain"},
                                      data=text).text)
        except:
            raise Exception("Error processing the request, HTTP: %d" % self.response.status_code)

