######################
# Author: Yifan Hong #
######################
from hashlib import sha256
from time import time

from django.shortcuts import render
from django.http import *
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import *
from django.db import IntegrityError, transaction
import json, traceback

from combatingSnake.settings import *
from models import User, Room
from errors import errors, RoomEmptyError
from utils import *


@csrf_exempt
def homePage(request):
    return render(request, 'index.html')

###########################

### utils

def fetch_user(request):
    '''Looks up user from X-Snake-Session-Id, and return him/her'''
    if SESSION_ID_HEADER not in request.META:
        raise errors.NOT_LOGGED_IN
    sessionId = request.META[SESSION_ID_HEADER]
    try:
        return User.find_by_session_id(sessionId)
    except ObjectDoesNotExist:
        raise errors.NOT_LOGGED_IN

def validate_master_key(request):
    '''
    Return true if request has valid master key, false otherwise.
    '''
    return request.META.get(MASTER_KEY_HEADER) == MASTER_KEY

def OKResponse(*args, **kwargs):
    '''
    Accept:
    OKResponse({'k':'v'})
    OKResponse(k = 'v')
    OKResponse({'k':'v'}, k = 'v')
    '''
    d = dict(kwargs)
    for arg in args:
        d.update(arg)
    return JsonResponse(d)

def getBooleanParam(request, key):
    val = request.GET.get(key, None)
    if val is None: return False
    try:
        return True if json.loads(val.lower()) else False
    except ValueError:
        traceback.print_exc();
        return False

def getIntegerParam(request, key, default = None):
    val = request.GET.get(key, default)
    try:
        return int(val)
    except ValueError:
        return default

### actual routes

class UsersView(View):
    '''
    /users path
    '''
    def post(self, request, *args, **kwargs):
        ''' reg user '''
        jsonbody = parse_json(request.body)
        try:
            user = User.from_dict(jsonbody).login().save();
        except IntegrityError as e:
            string = str(e)
            if 'UNIQUE' in string and 'username' in string: # try to identify the error
                return errors.USERNAME_TAKEN
            return errors.INTERNAL_SERVER_ERROR('{}: {}'.format(type(e).__name__, string))
        return OKResponse(userId = user.strId, sessionId = user.session_id)

    def delete(self, request, *args, **kwargs):
        '''
        Delete all users. For testing purposes only.
        '''
        if HEROKU_SERVER:
            raise errors.PERMISSION_DENIED
        if not validate_master_key(request):
            raise errors.PERMISSION_DENIED
        User.objects.all().delete()
        return OKResponse()


class UsersLoginView(View):
    '''
    /users/login
    '''
    def put(self, request, *args, **kwargs):
        ''' log user in '''
        args = sanitize_dict(parse_json(request.body), {'username':basestring, 'password':basestring})
        username, password = args['username'], args['password']
        try:
            user = User.find_by_username(username)
        except User.DoesNotExist:
            return errors.USERNAME_NOT_VALID('cannot find user {}'.format(username))
        if not user.check_password(password):
            return errors.INCORRECT_PASSWORD
        user.login().save()
        return OKResponse(userId = user.strId, sessionId = user.session_id)

    def delete(self, request, *args, **kwargs):
        ''' log user out '''
        try:
            user = fetch_user(request)
            user.logout().save()
        except errors.SnakeError as e:
            if e != errors.NOT_LOGGED_IN:
                raise e
            # as per the doc, logging out a non-existent session id has no effect
        return OKResponse()

class UsersScoresView(View):
    '''
    /users/scores path
    '''
    @transaction.atomic
    def put(self, request, *args, **kwargs):
        '''
        Update scores for a game. Require the POST body to be
        {'players':[list of user ids], 'winner':'user id of winner'}
        '''
        if not validate_master_key(request):
            return errors.PERMISSION_DENIED
        args = sanitize_dict(parse_json(request.body),
            required = {'players':list},
            optional = {'winner':basestring})
        User.update_scores(players = args.get('players'), winner = args.get('winner'));
        return OKResponse()

    def get(self, request, *args, **kwargs):
        '''
        Get leaderboard. Accept limit (default 20) and offset (default 0) as query
        args. Accept 'profile' and 'scores' as in getting single user. List will be ordered by
        the number of winned games.
        '''
        limit = getIntegerParam(request, 'limit', 20)
        if limit <= 0: limit = 20
        offset = getIntegerParam(request, 'offset', 0)
        if offset < 0: offset = 0
        includeProfile = getBooleanParam(request, 'profile')
        includeScores = getBooleanParam(request, 'scores')
        return OKResponse(users =
            [user.to_dict(includeProfile = includeProfile, includeScores = includeScores)
                for user in User.get_leaderboard()[offset:limit + offset]])

class SingleUserView(View):
    '''
    /users/:userId path; // https://docs.djangoproject.com/en/1.4/topics/class-based-views/#performing-extra-work
    '''
    def put(self, request, userId, *args, **kwargs):
        '''update profile or password'''
        user = fetch_user(request)
        if userId != user.strId:
            return errors.PERMISSION_DENIED
        user.update_profile(parse_json(request.body))
        return OKResponse()

    def get(self, request, userId, *args, **kwargs):
        ''' get user profile'''
        includeProfile = getBooleanParam(request, 'profile')
        includeScores = getBooleanParam(request, 'scores')
        user = User.find_by_id(str(userId))
        return OKResponse(user.to_dict(includeProfile = includeProfile, includeScores = includeScores))

    def delete(self, request, userId, *args, **kwargs):
        ''' delete a user. For testing purposes only; so requires master_key. '''
        if not validate_master_key(request):
            return errors.PERMISSION_DENIED
        User.find_by_id(str(userId)).delete()
        return OKResponse()

class SingleUserAuthenticateView(View):
    '''
    /users/:userId/authenticate
    '''
    def post(self, request, userId, *args, **kwargs):
        args = sanitize_dict(parse_json(request.body), {'ts':int, 'auth':basestring})
        ts, auth = args['ts'], args['auth']
        if abs(ts - time() * 1000) > 600000: # out of 10 mins
            return errors.TIMEOUT
        sessionId = User.find_by_id(userId).session_id
        rawAuth = "{}:{}:{}".format(sessionId, userId, ts)
        expectedAuth = sha256(rawAuth).hexdigest()
        if auth != expectedAuth:
            return errors.PERMISSION_DENIED
        return OKResponse()

class RoomsView(View):
    '''
    /rooms path
    '''

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        '''
        Create room
        '''
        user = fetch_user(request)
        room = Room.create_by(user).save()
        user.enter_room(room).save()
        return OKResponse(room.to_dict())

    def get(self, request, *args, **kwargs):
        '''
        Get all rooms
        '''
        includeCreatorProfile = getBooleanParam(request, 'creator-profile')
        includeMemberProfile = getBooleanParam(request, 'member-profile')
        includeMembers = includeMemberProfile or getBooleanParam(request, 'members')

        rooms = sorted(Room.all_rooms(), key = lambda r: r.roomId)
        return OKResponse(rooms = [room.to_dict(
            includeCreatorProfile = includeCreatorProfile,
            includeMembers = includeMembers,
            includeMemberProfile = includeMemberProfile) for room in rooms])

class SingleRoomView(View):
    '''
    /rooms/:roomId
    '''
    def get(self, request, roomId, *args, **kwargs):
        includeCreatorProfile = getBooleanParam(request, 'creator-profile')
        includeMemberProfile = getBooleanParam(request, 'member-profile')
        includeMembers = includeMemberProfile or getBooleanParam(request, 'members')

        room = Room.find_by_id(str(roomId))
        return OKResponse(room.to_dict(
            includeCreatorProfile = includeCreatorProfile,
            includeMembers = includeMembers,
            includeMemberProfile = includeMemberProfile))

    @transaction.atomic
    def put(self, request, roomId, *args, **kwargs):
        '''
        If argument 'status' is playing, requires a 'proposer'. If argument 'status'
        is waiting, just ends the game blindly.
        '''
        if not validate_master_key(request):
            return errors.PERMISSION_DENIED
        args = sanitize_dict(parse_json(request.body), {'status':int}, {'proposer':basestring})
        status, proposerId = args.get('status'), args.get('proposer')
        room = Room.find_by_id(roomId)
        print('Room {} is created by {} and proposed to start by {}'
            .format(room.roomId, room.creator.strId, proposerId))
        if status == STATUS_PLAYING and room.creator.strId != proposerId:
            return errors.PERMISSION_DENIED
        room.switch_status(status).save()
        return OKResponse()


class SingleRoomMembersView(View):
    '''
    /rooms/:roomId/members/
    '''
    def get(self, request, roomId, *args, **kwargs):
        includeMemberProfile = getBooleanParam(request, 'member-profile')
        room = Room.find_by_id(str(roomId))
        return OKResponse(room.to_dict(
            membersOnly = True,
            includeMemberProfile = includeMemberProfile));

class SingleRoomSingleMemberView(View):
    '''
    /rooms/:roomId/members/:memberId
    '''

    @transaction.atomic
    def put(self, request, roomId, memberId, *args, **kwargs):

        returnRoom = getBooleanParam(request, 'return-room')

        if validate_master_key(request):
            user = User.find_by_id(memberId)
        else:
            user = fetch_user(request)
            if memberId != user.strId:
                return errors.PERMISSION_DENIED
        room = Room.find_by_id(str(roomId)).raise_if_cannot_join(user)
        user.enter_room(room).save()

        if not returnRoom:
            return OKResponse()
        else:
            return OKResponse(Room.find_by_id(str(roomId)).to_dict(
                includeCreatorProfile = True,
                includeMembers = True,
                includeMemberProfile = True))

    @transaction.atomic
    def delete(self, request, roomId, memberId, *args, **kwargs):

        returnRoom = getBooleanParam(request, 'return-room')

        if validate_master_key(request):
            user = User.find_by_id(memberId)
        else:
            user = fetch_user(request)
            if memberId != user.strId:
                return errors.PERMISSION_DENIED
        room = Room.find_by_id(str(roomId))
        user.exit_room(room).save()
        try:
            room.reassign_creator_if_created_by(user).save()
        except RoomEmptyError:
            return OKResponse() # even if return-room is true

        if not returnRoom:
            return OKResponse()
        else:
            return OKResponse(Room.find_by_id(str(roomId)).to_dict(
                includeCreatorProfile = True,
                includeMembers = True,
                includeMemberProfile = True))

