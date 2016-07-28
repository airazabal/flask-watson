import requests
import json
import csv
import pickle
import urllib


'''
this is going to be a class responsible for wrapping calls to the FB API. 
It will start simply, with a hardcoded oauth token
It will make a call, getting back some simple fields
It will then pass those fields, packed or unpacked to whatever is needed. 
'''
class FbOauth(object):

    def __init__(self, token=None, fbid=None, testing=False):
        self.baseURL = 'https://graph.facebook.com/v2.7/'
        self.testing = testing
        if token == None:
            self.oauthToken = 'EAACEdEose0cBAGsqPN6EbMDWCnK9ikgSf7mg30ZCkOx9Q0ZAdgxGYo3OwqQpYOGadDTPJ936hKU4NiV7cTAvAjTaR99M43M9C23OGpgpyWG6uwZCR08CrF4o6Vp7mE9DNDS71ccX5tscGpgZBoQotqQ4TwmPxSe3jnZA5fQnGm11qDS6mQAFd'
        else:
            self.oauthToken = token
        if fbid == None:
            self.fbid = '129265874178799'
        else:
            self.fbid = fbid

    '''
	function that takes an oauth token, and a list of fields and returns the JSON from FB, or throws an error
	@param oauthToken: token for accessing the FB api
	@param fields: list of fields to include [<string>]
	@response json \/ error
	'''
    def get_fields(self, fields):
        return self.baseURL + str(self.fbid) + '/' + '?fields=' + '%2C'.join(fields) + '&access_token=%s' % (self.oauthToken)

    def fire_request(self, request_string):
    	if self.testing:
    		with open('data.json') as data_file:
    			data = json.load(data_file)
    		return data 
    	else:
    		return request.get(request_string).content
    # def get_feed(self):
    #     return self.baseURL + str(self.fbid) + '/' + 'feed?access_token=%s' % (self.oauthToken)
