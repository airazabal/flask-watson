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
        raise


def getUserID(access_token):
    try:
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        querystring = {
            "alt": "json",
            "access_token": access_token
        }
        return json.loads(requests.get(url, params=querystring).text)
    except Exception, e:
        raise


def getUserData(access_token):
    try:
        return getUserActivitiesList(getUserID(access_token)['id'], access_token)
    except Exception, e:
        raise


def getUserCommentsAsString(user_data):
    try:
        return ' '.join([cleanCommentString(x['object']['content']) for x in user_data['items']])
    except Exception, e:
        raise


def cleanCommentString(string):
    return string.encode('utf-8')
