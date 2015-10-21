from django.test import TestCase
from models import User
from hashing_passwords import *

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()

    def tearDown(self):
        User.objects.all().delete()
        
    def testCreateUserAndLogin(self):
        user = User.from_dict({
            'username': 'testUser',
            'password': 'password'
            }).login().save()
        print 'new user id {}'.format(user.hexId)
        self.assertIsNone(user.password)
        self.assertIsNotNone(user.pwhash)
        self.assertTrue(check_hash('password', user.pwhash),'check_hash for correct password')
        self.assertFalse(check_hash('passw0rd', user.pwhash),'check_hash for incorrect password')
        self.assertIsNotNone(user.session_id)
        
        user.logout().save()
        self.assertIsNone(user.session_id)
