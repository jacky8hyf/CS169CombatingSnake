######################
# Author: Yifan Hong #
######################

#
# Tests for views.py
#

# https://docs.djangoproject.com/en/1.8/topics/testing/tools/
from django.test import TestCase
from django.test import Client
from models import *
from django.core.exceptions import *
import json

from combatingSnake.settings import *
from errors import errors

class RestTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.sessionId = None
        self.masterKey = None
    def tearDown(self):
        self.sessionId = None
        self.masterKey = None

    def get(self, path, data=None, **extra):
        if self.sessionId:
            extra.update({SESSION_ID_HEADER : self.sessionId})
        if self.masterKey:
            extra.update({MASTER_KEY_HEADER : self.masterKey})
        response = self.c.get(path, data = data, **extra)
        return response

    def post(self, path, data = None, **extra):
        if self.sessionId:
            extra.update({SESSION_ID_HEADER : self.sessionId})
        if self.masterKey:
            extra.update({MASTER_KEY_HEADER : self.masterKey})
        extra.update({'data' : json.dumps(data) if data else None,
            'content_type' : 'application/json'})
        response = self.c.post(path, **extra)
        return response

    def put(self, path, data = None, **extra):
        if self.sessionId:
            extra.update({SESSION_ID_HEADER : self.sessionId})
        if self.masterKey:
            extra.update({MASTER_KEY_HEADER : self.masterKey})
        extra.update({'data' : json.dumps(data) if data else None,
            'content_type' : 'application/json'})
        response = self.c.put(path, **extra)
        return response
    def delete(self, path, **extra):
        if self.sessionId:
            extra.update({SESSION_ID_HEADER : self.sessionId})
        if self.masterKey:
            extra.update({MASTER_KEY_HEADER : self.masterKey})
        response = self.c.delete(path, **extra)
        return response

    def assertResponseSuccess(self, response, msg = None):
        '''
        Assert the response 2xx and 3xx, and return the parsed content
        '''
        self.assertLess(response.status_code, 400,
            'response is not successful with status code {} and content{}{}'
                .format(response.status_code,response.content,
                    ': {}'.format(msg) if msg else ''))
        return json.loads(response.content)

    def assertResponseFail(self, response, msg = None):
        '''
        Assert the response 4xx and 5xx, and return the parsed content
        '''
        self.assertGreaterEqual(response.status_code, 400,
            'response is successful with status code {} and content{}{}'
                .format(response.status_code,response.content,
                    ': {}'.format(msg) if msg else ''))
        d = json.loads(response.content)
        self.assertIn('err', d)
        return d

class SnakeRestTestCase(RestTestCase):
    def createUser(self, name):
        return self.assertResponseSuccess(self.post('/users', {'username':name,'password':'pass','nickname':name}));

class UsersViewTestCase(SnakeRestTestCase):

    def testRegLogin(self):
        d = self.assertResponseSuccess(self.post('/users', {'username':'user','password':'pass'}))
        self.assertIn('userId', d)
        self.assertIn('sessionId', d)
        userId = d['userId']
        oldSessionId = d['sessionId']
        d = self.assertResponseSuccess(self.put('/users/login', {'username':'user','password':'pass'}))
        self.assertIn('userId', d)
        self.assertIn('sessionId', d)
        self.assertEquals(userId, d['userId'])
        self.assertNotEquals(oldSessionId, d['sessionId'])

        self.sessionId = d['sessionId']
        d = self.assertResponseSuccess(self.delete('/users/login'))
        with self.assertRaises(ObjectDoesNotExist):
            print User.find_by_session_id(self.sessionId).session_id

        self.assertResponseSuccess(self.delete('/users/login'), 'logging out again should not fail')
        self.sessionId = 'Invalid id'
        self.assertResponseSuccess(self.delete('/users/login'), 'logging out with invalid session id should not fail')

        self.assertEquals(userId, User.find_by_id(userId).strId) # assert that delete does not delete the user

    def testRegLogin2(self):
        self.assertResponseSuccess(self.post('/users', {'username':'user','password':'pass'}))
        self.sessionId = self.assertResponseSuccess(self.put('/users/login', {'username':'user','password':'pass'}))['sessionId']
        d = self.assertResponseFail(self.put('/users/login', {'username':'user','password':'qass'}))
        self.assertEquals(errors.INCORRECT_PASSWORD.err, d['err'], 'Allows login with incorrect password')
        self.assertIsNotNone(User.find_by_session_id(self.sessionId))
        self.assertResponseSuccess(self.delete('/users/login'))
        self.assertResponseFail(self.put('/users/login', {'username':'user','password':'qass'}))
        self.assertResponseFail(self.put('/users/login', {'username':'user','password':'pass '}))
        with self.assertRaises(ObjectDoesNotExist):
            User.find_by_session_id(self.sessionId)
        self.assertResponseSuccess(self.put('/users/login', {'username':'user','password':'pass'}))['sessionId']

    def testDuplicateUsernameReg(self):
        self.assertResponseSuccess(self.post('/users', {'username':'user','password':'pass'}))
        d = self.assertResponseFail(self.post('/users', {'username':'user','password':'pass'}))
        self.assertEquals(errors.USERNAME_TAKEN.err, d['err'])

    def testUpdateProfile(self):
        pass # TODO tests for PUT /users/:userId

    def testUrlsPattern(self):
        k = 0
        userId = None
        while True:
            userId = self.assertResponseSuccess(self.post('/users', {'username':'user' + str(k),'password':'pass'}))['userId']
            k += 1
            toBreak = False
            for e in ('a','b','c','d','e','f'):
                if e in userId:
                    toBreak = True
                    break
            if toBreak:
                break
        anotherUserId = self.assertResponseSuccess(self.get('/users/' + userId))['userId']
        self.assertEquals(userId, anotherUserId)

    def testNotExist(self):
        body = self.assertResponseFail(self.get('/users/a'))
        self.assertEquals(errors.DOES_NOT_EXIST(None).err, body['err'])

    def testLoginNoUsername(self):
        resp = self.put('/users/login', {'username':'meow', 'password':'pwassdf'})
        body = self.assertResponseFail(resp)
        self.assertEquals(errors.USERNAME_NOT_VALID(None).err, body['err'])

    def testRegInvalidUsername(self):
        body = self.assertResponseFail(self.post('/users', {'username':'!!!!!!!!!','password':'pass'}))
        self.assertEquals(errors.USERNAME_NOT_VALID(None).err, body['err'])

    def testRegInvalidPassword(self):
        body = self.assertResponseFail(self.post('/users', {'username':'username','password':'1'}))
        self.assertEquals(errors.PASSWORD_NOT_VALID(None).err, body['err'])

    def testRegInvalidNickname(self):
        body = self.assertResponseFail(self.post('/users', {'username':'username','password':'pass', 'nickname':'g' * 65}))
        self.assertEquals(errors.NICKNAME_NOT_VALID(None).err, body['err'])

    def testScores(self):
        User.objects.all().delete()
        self.masterKey = MASTER_KEY
        alice, bob, catherine = self.createUser('iamalice'), self.createUser('iambob'), self.createUser('iamcatherine')
        aliceId, bobId, catherineId = alice['userId'], bob['userId'], catherine['userId']
        self.assertResponseFail(self.put('/users/scores',{'winner':catherineId}))
        self.assertResponseSuccess(self.put('/users/scores',{'players':[aliceId, bobId, catherineId]}))
        self.assertResponseSuccess(self.put('/users/scores',{'players':[aliceId, bobId, catherineId], 'winner':catherineId}))
        self.assertResponseSuccess(self.put('/users/scores',{'players':[aliceId, catherineId], 'winner':catherineId}))
        self.assertResponseSuccess(self.put('/users/scores',{'players':[aliceId, bobId], 'winner':bobId}))
        aliceObj, bobObj, catherineObj = User.find_by_id(aliceId), User.find_by_id(bobId), User.find_by_id(catherineId)
        self.assertEquals(4, aliceObj.numgames)
        self.assertEquals(0, aliceObj.numwin)
        self.assertEquals(3, bobObj.numgames)
        self.assertEquals(1, bobObj.numwin)
        self.assertEquals(3, catherineObj.numgames)
        self.assertEquals(2, catherineObj.numwin)
        lb = self.assertResponseSuccess(self.get('/users/scores', {'scores': True})).get('users')
        self.assertEquals(3, len(lb))
        self.assertEquals(lb, sorted(lb, key = lambda x: x['numwin'], reverse = True))

class RoomsViewTestCase(SnakeRestTestCase):
    def setUp(self):
        RestTestCase.setUp(self)
        self.user = self.alice = self.createUser('iamalice')
        self.bob = self.createUser('iambob')
        self.iAmAlice()

    def iAmAlice(self):
        self.sessionId = self.alice['sessionId']
    def iAmBob(self):
        self.sessionId = self.bob['sessionId']
    def iAm(self, user):
        self.sessionId = user['sessionId']

    def testCreateBy(self):
        d = self.assertResponseSuccess(self.post('/rooms'))
        self.assertEquals(self.user['userId'], d['creator']['userId'])
        self.assertIn('roomId', d)
        self.assertTrue(d['roomId'], '{} is False or empty'.format(d['roomId']))

    def testGetRooms(self):
        roomIds = []
        for i in range(20):
            user = self.createUser('user' + str(i))
            self.iAm(user)
            roomIds.append(self.assertResponseSuccess(self.post('/rooms'))['roomId'])


        gotArray = self.assertResponseSuccess(self.get('/rooms'))['rooms']
        gotRoomIds = [e['roomId'] for e in gotArray]
        self.assertEquals(set(roomIds), set(gotRoomIds), 'GET /rooms doesn\'t match: expected {}, got {}'.format(roomIds, gotRoomIds))
        self.assertEquals(len(roomIds), len(gotRoomIds), 'GET /rooms size doesn\'t match: expected {}, got {}'.format(roomIds, gotRoomIds))

        gotArrayLookup = dict()
        for e in gotArray:
            gotArrayLookup[e['roomId']] = e

        for roomId in roomIds:
            gotRoom = self.assertResponseSuccess(self.get('/rooms/' + roomId))
            self.assertEquals(gotArrayLookup[roomId], gotRoom)

    def testJoinExitRoom(self):
        catherine = self.createUser('iamcatherine')
        self.iAmAlice()
        room = self.assertResponseSuccess(self.post('/rooms'))
        roomId = room['roomId']
        self.iAmBob()
        self.assertResponseSuccess(self.put('/rooms/' + roomId + '/members/' + self.bob['userId']))
        self.assertIsNotNone(User.find_by_id(self.bob['userId']).inroom)
        self.assertEquals(roomId, User.find_by_id(self.bob['userId']).inroom.strId)

        gotUserId = self.assertResponseSuccess(self.get('/rooms/' + roomId, {'members': True}))['members'][0]['userId'];
        self.assertEquals(self.bob['userId'], gotUserId)

        self.iAm(catherine)
        anotherRoomId = self.assertResponseSuccess(self.post('/rooms'))['roomId']
        self.iAmBob()
        self.assertResponseSuccess(self.delete('/rooms/' + anotherRoomId + '/members/' + self.bob['userId']))
        self.assertIsNotNone(User.find_by_id(self.bob['userId']).inroom, 'exiting a wrong room should not have effects')
        self.assertEquals(roomId, User.find_by_id(self.bob['userId']).inroom.strId, 'exiting a wrong room should not have effects')

        # bob exit it
        self.assertResponseSuccess(self.delete('/rooms/' + roomId + '/members/' + self.bob['userId']))
        self.assertIsNone(User.find_by_id(self.bob['userId']).inroom)
        gotMembers = self.assertResponseSuccess(self.get('/rooms/' + roomId, {'members': True}))['members']
        self.assertEquals(0, len(gotMembers))

        # bob enter again
        self.assertResponseSuccess(self.put('/rooms/' + roomId + '/members/' + self.bob['userId']))
        # alice exit it
        self.iAmAlice()
        self.assertResponseSuccess(self.delete('/rooms/' + roomId + '/members/' + self.alice['userId']))
        roomObj = Room.find_by_id(roomId)
        # print roomObj.to_dict(includeMembers = True, includeMemberProfile = True)
        self.assertEquals(self.bob['userId'], roomObj.creator.strId, 'Bob is not creator when old creator exits it')
        self.assertFalse(roomObj.all_members)

        self.iAmBob()
        self.assertResponseSuccess(self.delete('/rooms/' + roomId + '/members/' + self.bob['userId']))
        with self.assertRaises(ObjectDoesNotExist):
            Room.find_by_id(roomId)
        self.assertIsNone(User.find_by_id(self.bob['userId']).inroom, 'bob should not be in the room')

    def testParams(self):
        self.iAmAlice()
        room = self.assertResponseSuccess(self.post('/rooms'))
        roomId = room['roomId']
        self.iAmBob()
        self.assertResponseSuccess(self.put('/rooms/' + roomId + '/members/' + self.bob['userId']))

        d = self.assertResponseSuccess(self.get('/rooms/' + roomId, {'creator-profile': True}))
        self.assertIn('creator',d)
        self.assertIn('nickname',d['creator'])
        self.assertEquals('iamalice', d['creator']['nickname'])

        d = self.assertResponseSuccess(self.get('/rooms/' + roomId, {'members': True}))
        self.assertIn('members', d)
        members = d['members']
        self.assertIsInstance(members, list)
        self.assertEquals(1, len(members))
        self.assertEquals(self.bob['userId'], d['members'][0]['userId'])

        d = self.assertResponseSuccess(self.get('/rooms/' + roomId, {'member-profile': True}))
        self.assertIn('members', d)
        members = d['members']
        self.assertIsInstance(members, list)
        self.assertEquals(1, len(members))
        self.assertEquals(self.bob['userId'], d['members'][0]['userId'])
        self.assertEquals('iambob', d['members'][0]['nickname'])

        d = self.assertResponseSuccess(self.get('/rooms/' + roomId, {'members':False, 'creator-profile':False,'member-profile': False}))
        self.assertNotIn('members', d)
        self.assertNotIn('nickname',d['creator'])

        d = self.assertResponseSuccess(self.get('/rooms/' + roomId, {'members':True, 'creator-profile':False,'member-profile': False}))
        self.assertNotIn('nickname', d['members'][0])
        self.assertNotIn('nickname',d['creator'])


    def testUrls(self):
        resp = self.put('/rooms/a/members/b')
        self.assertNotEquals(405, resp.status_code)

    def testNotExist(self):
        body = self.assertResponseFail(self.get('/rooms/a'))
        self.assertEquals(errors.DOES_NOT_EXIST(None).err, body['err'])

    def testJoinFullRoom(self):
        self.iAmAlice()
        room = self.assertResponseSuccess(self.post('/rooms'))
        roomId = room['roomId']

        users = [self.createUser('user' + str(i)) for i in range(room['capacity'] - 1)]
        for u in users: # -1 for creator
            self.iAm(u)
            self.assertResponseSuccess(self.put('/rooms/' + roomId + '/members/' + u['userId']))
        self.iAmBob()
        d = self.assertResponseFail(self.put('/rooms/' + roomId + '/members/' + self.bob['userId']))
        self.assertEquals(errors.ROOM_FULL.err, d['err'])

    def testJoinPlayingRoom(self):
        self.iAmAlice()
        room = self.assertResponseSuccess(self.post('/rooms'))
        roomId = room['roomId']

        Room.find_by_id(roomId).switch_status(STATUS_PLAYING).save()

        self.iAmBob()
        d = self.assertResponseFail(self.put('/rooms/' + roomId + '/members/' + self.bob['userId']))
        self.assertEquals(errors.ROOM_PLAYING.err, d['err'])

    def testJoinMyOwnRoom(self):
        room = self.assertResponseSuccess(self.post('/rooms'))
        roomId = room['roomId']
        self.assertResponseSuccess(self.put('/rooms/' + roomId + '/members/' + self.user['userId']))

    def testAbnormalExit(self):
        catherine = self.createUser('iamcatherine')

        self.iAmAlice()
        roomId = self.assertResponseSuccess(self.post('/rooms'))['roomId']

        self.iAm(catherine)
        roomId2 = self.assertResponseSuccess(self.post('/rooms'))['roomId']

        self.iAmBob()
        self.assertResponseSuccess(self.put('/rooms/' + roomId + '/members/' + self.bob['userId']))
        members = self.assertResponseSuccess(self.get('/rooms/' + roomId, {'members': True}))['members']
        self.assertEquals(1, len(members))

        # entering room2 exits room 1
        self.assertResponseSuccess(self.put('/rooms/' + roomId2 + '/members/' + self.bob['userId']))
        members = self.assertResponseSuccess(self.get('/rooms/' + roomId, {'members': True}))['members']
        self.assertEquals(0, len(members))

        self.iAmAlice()
        self.assertResponseSuccess(self.put('/rooms/' + roomId2 + '/members/' + self.alice['userId']))
        d = self.assertResponseFail(self.get('/rooms/' + roomId))
        self.assertEquals(errors.DOES_NOT_EXIST('').err, d['err'])


    def testAbnormalExit2(self):
        self.iAmAlice()
        roomId = self.assertResponseSuccess(self.post('/rooms'))['roomId']
        roomId2 = self.assertResponseSuccess(self.post('/rooms'))['roomId']
        d = self.assertResponseFail(self.get('/rooms/' + roomId))
        self.assertEquals(errors.DOES_NOT_EXIST('').err, d['err'])

    def testEnterSameRoom(self):
        self.iAmAlice()
        roomId = self.assertResponseSuccess(self.post('/rooms'))['roomId']
        self.assertResponseSuccess(self.put('/rooms/' + roomId + '/members/' + self.alice['userId']))
        self.assertResponseSuccess(self.put('/rooms/' + roomId + '/members/' + self.alice['userId']))