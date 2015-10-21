from django.test import TestCase
from models import User
from hashing_passwords import *

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()

    def tearDown(self):
        User.objects.all().delete()

    def testUserSetPassword(self):
        user = User()
        setattr(user, 'password', 'good')
        self.assertTrue(user.pwhash, 'pwhash is empty: {}'.format(user.pwhash))

    def testCreateUserAndLogin(self):
        user = User.from_dict({
            'username': 'testUser',
            'password': 'password'
            }).login().save()
        print 'new user id {}'.format(user.hexId)
        self.assertIsNone(user.password)
        self.assertTrue(user.pwhash)
        self.assertTrue(user.check_password('password'),'check_password for correct password: {}'.format(user.pwhash))
        self.assertFalse(user.check_password('passw0rd'),'check_hash for incorrect password {}'.format(user.pwhash))
        self.assertIsNotNone(user.session_id)
        self.assertEquals(User.find_by_session_id(user.session_id), user, 'User found by session_id is different {}'.format(user.session_id))
        user.logout().save()
        self.assertIsNone(user.session_id)

    def testUpdateProfile(self):
        user = User.from_dict({
            'username': 'testUser',
            'password': 'password'
            })
        user.update_profile({
            'username':'danger',
            'session_id':'double_trouble',
            'pwhash':'alright'
            })
        self.assertEquals('testUser', user.username , 'username should not be updated')
        self.assertIsNone(user.session_id, 'session_id should not be updated')
        self.assertTrue(user.check_password('password'),'pwhash should not be updated')

        user.update_profile({
            'password':'danger'
            })
        self.assertIsNone(user.password)
        self.assertTrue(user.check_password('danger'),'check_password for new password: {}'.format(user.pwhash))
        self.assertFalse(user.check_password('password'),'check_password for old password: {}'.format(user.pwhash))

        user.update_profile({
            'nickname':'meow'
            })
        self.assertEquals('meow', user.nickname)

        user.update_profile({})
        self.assertEquals('testUser', user.username)
        self.assertTrue(user.check_password('danger'),'check_password for new password: {}'.format(user.pwhash))
        self.assertEquals('meow', user.nickname)

