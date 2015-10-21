from django.shortcuts import render
from django.http import *
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import *
from django.db import IntegrityError

from models import User, Room
from errors import errors
from utils import *

# Create your views here.
def gameStart(request):
    return render(request, 'snake.html')

@csrf_exempt
def homePage(request):
    return render(request, 'index.html')

###########################

### utils

def fetch_user(request):
    '''Looks up user from X-Snake-Session-Id, and return him/her'''
    if 'X-Snake-Session-Id' not in request.META:
        raise errors.NOT_LOGGED_IN
    sessionId = request.META['X-Snake-Session-Id']
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
        except IntegrityError:
            return errors.USERNAME_TAKEN
        return OKResponse(userId = user.strId, sessionId = user.session_id)

class UsersLoginView(View):
    '''
    /users/login
    '''
    def put(self, request, *args, **kwargs):
        ''' log user in '''
        args = sanitize_dict(parse_json(request.body), {'username':basestring, 'password':basestring})
        username, password = args['username'], args['password']
        user = User.find_by_username(username)
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
        includeProfile = request.GET.get('profile', False)
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
        includeCreatorProfile = request.GET.get('creator-profile', False)
        includeMemberProfile = request.GET.get('member-profile', False)
        includeMembers = includeMemberProfile or request.GET.get('members', False)

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
        includeCreatorProfile = request.GET.get('creator-profile', False)
        includeMemberProfile = request.GET.get('member-profile', False)
        includeMembers = includeMemberProfile or request.GET.get('members', False)

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
        includeMemberProfile = request.GET.get('member-profile', False)
        room = Room.find_by_id(str(roomId))
        return OKResponse(room.to_dict(
            membersOnly = True,
            includeMemberProfile = includeMemberProfile));

class SingleRoomSingleMemberView(View):
    '''
    /rooms/:roomId/members/:memberId
    '''
    def put(self, request, roomId, memberId, *args, **kwargs):
        user = fetch_user(request)
        if memberId != user.strId:
            return errors.PERMISSION_DENIED
        room = Room.find_by_id(str(roomId))
        user.enter_room(room)
        return OKResponse()
    def delete(self, request, roomId, memberId, *args, **kwargs):
        user = fetch_user(request)
        if memberId != user.strId:
            return errors.PERMISSION_DENIED
        room = Room.find_by_id(str(roomId))
        user.exit(room)
        return OKResponse()

