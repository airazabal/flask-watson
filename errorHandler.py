from flask import jsonify

'''
Standard error handling class.
Registered in server.py

Usage is simple.

in your view function:
raise StandardError(message, status_code, payload)

Based on http://flask.pocoo.org/docs/0.11/patterns/apierrors/

'''


class ErrorHandler(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
