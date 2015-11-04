######################
# Author: Yifan Hong #
######################

from django.shortcuts import render
from django.http import *
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import *
from django.db import IntegrityError, transaction
import json, traceback

from .models import User, Room
from .errors import errors
from .utils import *

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
    if isinstance(val, bytes):
        val = val.decode("utf-8")
    if not val: return False
    try:
        return True if json.loads(val.lower()) else False
    except ValueError:
        traceback.print_exc();
        return False

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

class UsersLoginView(View):
    '''
    /users/login
    '''
    def put(self, request, *args, **kwargs):
        ''' log user in '''
        args = sanitize_dict(parse_json(request.body), {'username':str, 'password':str})
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
        user = User.find_by_id(str(userId))
        return OKResponse(user.to_dict(includeProfile = includeProfile))

class RoomsView(View):
    '''
    /rooms path
    '''
    def post(self, request, *args, **kwargs):
        '''
        Create room
        '''
        user = fetch_user(request)
        room = Room.create_by(user).save()
        return OKResponse(room.to_dict())

    def get(self, request, *args, **kwargs):
        '''
        Get all rooms
        '''
        includeCreatorProfile = getBooleanParam(request, 'creator-profile')
        includeMemberProfile = getBooleanParam(request, 'member-profile')
        includeMembers = includeMemberProfile or getBooleanParam(request, 'members')

        rooms = Room.all_rooms()
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
        user = fetch_user(request)
        if memberId != user.strId:
            return errors.PERMISSION_DENIED
        room = Room.find_by_id(str(roomId)).raise_if_cannot_join(user)
        user.enter_room(room).save()
        return OKResponse()

    @transaction.atomic
    def delete(self, request, roomId, memberId, *args, **kwargs):
        user = fetch_user(request)
        if memberId != user.strId:
            return errors.PERMISSION_DENIED
        room = Room.find_by_id(str(roomId))
        user.exit_room(room).save()
        room.destroy_if_created_by(user)
        return OKResponse()

