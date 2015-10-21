from django.test import TestCase
from models import *
from hashing_passwords import *
from django.core.exceptions import *

class UserTestCase(TestCase):
    # no need to clear user table, as django test clears the in-memory
    # database each time

    def testUserSetPassword(self):
        user = User()
        setattr(user, 'password', 'good')
        self.assertTrue(user.pwhash, 'pwhash is empty: {}'.format(user.pwhash))

    def testCreateUserAndLogin(self):
        user = User.from_dict({
            'username': 'testUser',
            'password': 'password'
        }).login().save()
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

    def testToDict(self):
        user = User.from_dict({
            'username': 'testUser',
            'password': 'password'
        })
        d = user.to_dict()
        self.assertIn('userId', d)
        self.assertNotIn('password', d)
        self.assertNotIn('pwhash', d)
        self.assertNotIn('session_id', d)
        self.assertNotIn('nickname', d)

        d = user.to_dict(includeProfile = True)
        self.assertIn('userId', d)
        self.assertIn('nickname', d)

    def testRooms(self):
        pass # TODO test find_by_inroom, enter_room, exit_room, all_members

    def testFinds(self):
        users = [User.from_dict({
            'username': 'user{}'.format(i),
            'password': 'password'
        }).login().save() for i in range(10)]

        for expectUser in users:
            self.assertEquals(expectUser, User.find_by_username(expectUser.username))
            self.assertEquals(expectUser, User.find_by_session_id(expectUser.session_id))


class RoomTestCase(TestCase):
    def setUp(self):
        self.user = User.from_dict({
            'username': 'user',
            'password': 'password',
            'nickname': 'nick'
        }).login().save()

    def testCreateBy(self):
        room = Room.create_by(self.user)
        self.assertEquals(self.user, room.creator)

        with self.assertRaises(ValueError):
            Room.create_by(None).save()

        d = room.to_dict()
        for key in ('roomId','capacity','status','creator'):
            self.assertIn(key, d)
        self.assertNotIn('nickname', d['creator'])
        self.assertNotIn('members', d)

        d = room.to_dict(includeCreatorProfile = True)
        self.assertIn('nickname', d['creator'])

        d = room.to_dict(includeMembers = True)
        self.assertIn('members',d)

    def testAllRoomsAndFind(self):
        rooms = [Room.create_by(self.user).save() for _ in range(10)]
        self.assertEquals(set(rooms), set(Room.all_rooms()))
        for room in rooms:
            self.assertEquals(room, Room.find_by_id(room.roomId))

    def testConflictUsername(self):
        User.from_dict({
            'username': 'user',
            'password': 'password',
            'nickname': 'nick'
        }).save()
        with self.assertRaises(IntegrityError):
            User.from_dict({
                'username': 'user',
                'password': 'password',
                'nickname': 'nick'
            }).save()
