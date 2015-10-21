# https://docs.djangoproject.com/en/1.8/topics/testing/tools/
from django.test import TestCase
from django.test import Client
from models import *
import json

class RestTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.sessionId = None

    def get(self, path, data=None, **extra):
        if self.sessionId:
            extra.update({'X-Snake-Session-Id' : self.sessionId})
        response = self.c.get(path, data = data, **extra)
        return response

    def post(self, path, data = None, **extra):
        if self.sessionId:
            extra.update({'X-Snake-Session-Id' : self.sessionId})
        extra.update({'data' : json.dumps(data) if data else None,
            'content_type' : 'application/json'})
        response = self.c.post(path, **extra)
        return response

    def put(self, path, data = None, **extra):
        if self.sessionId:
            extra.update({'X-Snake-Session-Id' : self.sessionId})
        extra.update({'data' : json.dumps(data) if data else None,
            'content_type' : 'application/json'})
        response = self.c.put(path, **extra)
        return response
    def delete(self, path, **extra):
        if self.sessionId:
            extra.update({'X-Snake-Session-Id' : self.sessionId})
        response = self.c.delete(path, **extra)
        return response

    def assertSuccessfulResponse(self, response):
        self.assertLess(response.status_code, 400,
            'response is not successful with status code {}'.format(response.status_code))
        return json.loads(response.content)

class UsersViewTestCase(RestTestCase):

    def testRegLogin(self):
        d = self.assertSuccessfulResponse(self.post('/users', {'username':'user','password':'pass'}))
        self.assertIn('userId', d)
        self.assertIn('sessionId', d)

        oldSessionId = d['sessionId']
        d = self.assertSuccessfulResponse(self.put('/users/login', {'username':'user','password':'pass'}))
        self.assertIn('userId', d)
        self.assertIn('sessionId', d)

        self.assertNotEquals(oldSessionId, d['sessionId'])


