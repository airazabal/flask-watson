import requests
import json
import urllib


'''
this is going to be a class responsible for wrapping calls to the FB API.
It will start simply, with a hardcoded oauth token
It will make a call, getting back some simple fields
It will then pass those fields, packed or unpacked to whatever is needed.
'''


class FbOauth(object):

    def __init__(self, token, fbid):
        self.baseURL = 'https://graph.facebook.com/v2.7/'
        self.token = token
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
            '%2C'.join(fields) + '&access_token=%s' % (self.token)
    '''
    wrapper for firing a request in the testing context
    takes in a request string
    if the object is testing, then it simply returns the json stored locally
    else it fires the composed request, and returns the content
    '''

    def fire_request(self, request_string):
        return requests.get(request_string).content
