from django.shortcuts import render
from models import User, Room
from django.http import *
from django.views.generic import View
import json
from errors import errors
from utils import *

# Create your views here.
def gameStart(request):
    return render(request, 'snake.html')

def homePage(request):
    return render(request, 'index.html')

###########################

### utils

def fetch_user(request):
    '''Looks up user from X-Snake-Session-Id, and return him/her'''
    return User()

def OKResponse(**kwargs):
	d = dict(kwargs)
	return JsonResponse(d)

### actual routes

class UsersView(View):
    '''
    /users path
    '''
    def post(self, request):
        ''' reg user '''
        jsonbody = parse_json(request.body)
        user = User.from_dict(jsonbody)
        # FIXME check user is not None
        # FIXME log him/her in
        user.save()
        # FIXME fetch the id and session_id
        return OKResponse({'user': 'User has been created'})
        #return errors.NOT_IMPLEMENTED # FIXME return the id and session_id

class UsersLoginView(View):
    '''
    /users/login
    '''
    def put(self, request):
        ''' log user in '''
        jsonbody = parse_json(request.body);
        username, password = jsonbody['username'], jsonbody['password']
        # FIXME if either are none return error
        # FIXME log user in
        return errors.NOT_IMPLEMENTED # FIXME return user id and session_id
    def delete(self, request, *args, **kwargs):
        ''' log user out '''
        return errors.NOT_IMPLEMENTED # FIXME log user out and return {}

class SingleUserView(View):
    '''
    /users/:userId path; // https://docs.djangoproject.com/en/1.4/topics/class-based-views/#performing-extra-work
    '''
    def putSingleUser(self, request, userId):
        '''update profile or password'''
        user = fetch_user(request)
        # FIXME assert user exists
        user.update_profile(parse_json(request.body))
        return errors.NOT_IMPLEMENTED # FIXME return {}

class RoomsView(View):
    '''
    /rooms path
    '''
    def post(self, request):
        user = fetch_user(request)
        # FIXME assert user exists
        room = Room.createBy(user)
        return errors.NOT_IMPLEMENTED # FIXME save it and return its json dump
    def get(self, request):
        includeCreatorProfile = request.GET.get('creator-profile', False)
        includeMembers = request.GET.get('members', False)
        return errors.NOT_IMPLEMENTED # FIXME get rooms and return its json dump

class SingleRoomView(View):
    '''
    /rooms/:roomId
    '''
    def get(self, request, roomId):
        includeCreatorProfile = request.GET.get('creator-profile', False)
        includeMembers = request.GET.get('members', False)
        includeMemberProfile = request.GET.get('member-profile', False)
        return errors.NOT_IMPLEMENTED # FIXME get from data base and dump to json

class SingleRoomMembersView(View):
    '''
    /rooms/:roomId/members/
    '''
    def get(self, request, roomId):
        includeMembers = request.GET.get('members', False)
        includeMemberProfile = request.GET.get('member-profile', False)
        return errors.NOT_IMPLEMENTED # FIXME get from data base and dump to json

class SingleRoomMemberView(View):
    '''
    /rooms/:roomId/members/:memberId
    '''
    def put(self, request, roomId, memberId):
        user = fetch_user(request)
        # FIXME assert user exists
        # FIXME assert memberId matches user.id
        # FIXME set user.inroom
        return errors.NOT_IMPLEMENTED # return {}
    def delete(self, request, roomId, memberId):
        user = fetch_user(request)
        # FIXME assert user exists
        # FIXME assert memberId matches user.id
        # FIXME set user.inroom
        return errors.NOT_IMPLEMENTED # return {}
