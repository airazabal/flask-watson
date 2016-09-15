import json
import os
from watsoncaller.personality_insights_wrapper import PersonalityInsight
from errors import ErrorHandler

def check_fields(needed, data):
    if data is None:
        raise ErrorHandler("You must send data with the request")
    missing = ','.join(list(set(needed)-set(data.keys())))
    if (len(missing)>0):
        raise ErrorHandler('Your call is missing the following parameters: [%s]' % (missing))



def json_validation(json_data):
    try:
        return json.loads(json.dumps(json_data))
    except:
        raise Exception("Bad Data")


def pi_instantiation(mock=False):
    if mock:
        return PersonalityInsight({'MOCK': True, 'username': True,
                                   'password': True, 'url': True})
    else:
        try:
            username = os.getenv('PIUsername')
            password = os.getenv('PIPassword')
            url = os.getenv('PIUrl')
            return PersonalityInsight({'username': username,
                                       'password': password, 'url': url})
        except:
            raise Exception("environment variables dont exist")

''' 
Helper method to unpack posts from facebook data return.  
Needs to be extended to handle multiple pages of data. 
Accepts data in a json format (see _resources/data.json_). 
Returns a string to be passed to Personality Insights. 

'''

def unpack_fb_posts(data):
    try:
        myS = ''
        for item in data['posts']['data']:
            try:
                myS = myS + ' ' + item['message']
            except:
                pass
        return myS.encode('utf-8')
    except Exception, e:
        raise Exception(str(e) + '  no posts were found')
     
def unpack_tweets(tw_data):
    try:
        twStr = ''
        for tweet in range(0, len(tw_data)):
            twStr = twStr + ' ' + tw_data[tweet]['text']
        return twStr
    except Exception, e:
        raise Exception(str(e) + ' no tweets were found')
