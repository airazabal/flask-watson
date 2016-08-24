import requests
import json


def getUserActivitiesList(user_id, access_token):
    try:
        url = "https://www.googleapis.com/plus/v1/people/%s/activities/public" % (
            user_id)
        querystring = {
            "access_token": access_token
        }
        return json.loads(requests.get(url, params=querystring).text)
    except Exception, e:
        print str(e)
        print 'failed to get user activites list'
        raise Exception


def getUserID(access_token):
    try:
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        querystring = {
            "alt": "json",
            "access_token": access_token
        }
        return json.loads(requests.get(url, params=querystring).text)

    except Exception, e:
        print str(e)
        print 'failed to get user data'
        raise Exception


def getUserData(access_token):
    try:
        return getUserActivitiesList(getUserID(access_token)['id'], access_token)
    except Exception, e:
        print str(e)
        raise Exception


def getUserCommentsAsString(user_data):
    try:
        return ' '.join([str(x['object']['content'].replace(u'\ufeff', ' ').replace(u'<br />', ' ').replace(u'&#39;', ' ')) for x in user_data['items']])
    except Exception, e:
        print str(e)
