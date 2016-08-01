import json
import os
from watsoncaller.personality_insights_wrapper import PersonalityInsight


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
