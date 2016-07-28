import requests
import json
import csv
import pickle
import urllib
import urllib

class MockPersonalityInsight:

    def return_text(self):
        file = open("insights.pickle","rb")
        object_file = pickle.load(file)
        file.close()
        return object_file

class PersonalityInsight(object):

    def __new__(cls, text, credentials={}):
        check_values = ['username', 'password', 'url']
        if all(value in credentials.keys() for value in check_values) and text != None: 
            if 'MOCK' in credentials.values():
                return MockPersonalityInsight()
            else:
                return super(PersonalityInsight, cls).__new__(cls, text, credentials)    
        else :
            raise ValueError('Illegal Argument Exception')

    def __init__(self, text, credentials):
        self.username = credentials['username']
        self.password = credentials['password']
        self.url = credentials['url']
        self.personality = {}
        self.text = text

    def return_text(self):
        '''Url specifies the url you are sending this request to. auth is your authorization to use that url. 
        Headers specifies that the content type is just a block of plain text.
        Many optional parameters, such as language of input, language of output, etc, are left out.
        Data is the text we are analyzing. It must be atleast 100 words long'''
        self.response = requests.post(self.url + "/v2/profile",
                                      auth=(self.username, self.password),
                                      headers={"content-type": "text/plain"},
                                      data=self.text)
        try:
            #response.text decodes the response into a JSON object
            self.personality = json.loads(self.response.text)
            #Personality is now a dictionary containing all the response fields
            return self.personality
        except:
            raise Exception("Error processing the request, HTTP: %d" % self.response.status_code)

class PersonalityInsightCaller:

    def __init__(self, credentials):
        self.credentials = credentials
        self.text = None

    def insert_text(self, text):
        self.text = text

    def get_personality(self):
        #create a personalityInsight object
        PIobject = PersonalityInsight(self.text, self.credentials)
        
        #get the personality "text" from that personality insight object 
        response = PIobject.return_text()
        return response
