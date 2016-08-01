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
        if token is None:
            self.oauthToken = 'EAACEdEose0cBAGsqPN6EbMDWCnK9ikgSf7mg30ZCkOx9Q0ZAdgxGYo3OwqQpYOGadDTPJ936hKU4NiV7cTAvAjTaR99M43M9C23OGpgpyWG6uwZCR08CrF4o6Vp7mE9DNDS71ccX5tscGpgZBoQotqQ4TwmPxSe3jnZA5fQnGm11qDS6mQAFd'
        else:
            self.oauthToken = token
        if fbid is None:
            self.fbid = '129265874178799'
        else:
            self.fbid = fbid

    '''
    wrapper of the get_fields and fire_request functions
    '''

    def get_fb_data(self, fields):
        return self.fire_request(self.get_fields(fields))

    '''
	function that takes an oauth token, and a list of fields and returns the query string
	@param fields: list of fields to include [<string>]
	@response api query string
	'''

    def get_fields(self, fields):
        return self.baseURL + str(self.fbid) + '/' + '?fields=' + \
            '%2C'.join(fields) + '&access_token=%s' % (self.oauthToken)
    '''
    wrapper for firing a request in the testing context
    takes in a request string
    if the object is testing, then it simply returns the json stored locally
    else it fires the composed request, and returns the content
    '''

    def fire_request(self, request_string):
        if self.testing:
            with open('resources/data.json') as data_file:
                data = json.load(data_file)
            return data
        else:
            return requests.get(request_string).content
