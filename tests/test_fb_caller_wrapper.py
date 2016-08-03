from fbcaller.fbOauth import FbOauth
import unittest
import json

class TestFacebookRequest(unittest.TestCase):
	def test_form_call(self):
		token = "123ABC"
		fbid = '123456778'
		myFb = FbOauth(token=token,fbid=fbid)
		expected = 'https://graph.facebook.com/v2.7/123456778/?fields=name%2Cemail%2Cposts&access_token=123ABC'
		self.assertEqual(expected, myFb.get_fields(['name', 'email', 'posts']))


	def test_api_call_with_failure(self):
		token = '123ABC'
		fbid = '123456778'
		myFb = FbOauth(token=token,fbid=fbid)
		expected1 = ['error']
		errorObj = myFb.get_fb_data(['name', 'email', 'posts'])
		self.assertEqual(expected1,errorObj.keys())
		expected2 = ['message', 'code', 'type', 'fbtrace_id']
		self.assertEqual(expected2, errorObj['error'].keys())



if __name__ == "__main__":
    unittest.main()
    