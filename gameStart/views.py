from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.views.generic import View
import json

# Create your views here.
def gameStart(request):
    return render(request, 'snake.html')

def homePage(request):
    return render(request, 'index.html')

def renderRegister(request):
    return render(request, 'registration_form.html')

def renderLogin(request):
    return render(request, 'login.html')

def createUser(request):
    assert request.method == 'POST', "createUser must be a POST request"
    requestData = json.loads(request.body) # decode the request data into a dictionary
    username = requestData['username']
    email = requestData['email']
    password = requestData['password']

    user = User.objects.create_user(username, email, password)
    response = {}
    response["status"] = 1
    response["msg"] = ""
    return HttpResponse(json.dumps(response), content_type='application/json')

def changePassword(request):
    assert request.method == 'POST', "changePassword must be a POST request"
    requestData = json.loads(request.body) # decode the request data into a dictionary
    username = requestData['username']
    newPassword = requestData['newPassword']

    user = User.objects.get(username=username)
    user.set_password(newPassword)
    response = {}
    response["status"] = 1
    response["msg"] = ""
    return HttpResponse(json.dumps(response), content_type='application/json')

def login(request):
    assert request.method == 'GET', "login must be a GET request"
    requestData = json.loads(request.body) # decode the request data into a dictionary
    username = requestData['username']
    password = requestData['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            print("user is valid, active and aunthenticated")
        else:
            print("The password is valid, but the account has been disabled")
    else:
        print("The username and password were incorrect")

    response = {}
    response["status"] = 1
    response["msg"] = ""
    return HttpResponse(json.dumps(response), content_type='application/json')

###########################

class UsersView(View):
    '''
    /users path
    '''
    def post(self, request):
        pass

class UsersLoginView(View):
    '''
    /users/login
    '''
    def put(self, request, *args, **kwargs):
        pass
    def delete(self, request, *args, **kwargs):
        pass

class SingleUserView(View):
    '''
    /users/:userId path; // https://docs.djangoproject.com/en/1.4/topics/class-based-views/#performing-extra-work
    '''
    def putSingleUser(self, request, userId):
        pass

class RoomsView(View):
    '''
    /rooms path
    '''
    def post(self, request, *args, **kwargs):
        pass
    def get(self, request, *args, **kwargs):
        pass

class SingleRoomView(View):
    '''
    /rooms/:roomId
    '''
    def get(self, request, roomId):
        pass



class SingleRoomMembersView(View):
    '''
    /rooms/:roomId/members/
    '''
    def get(self, request, roomId):
        pass
    
class SingleRoomMemberView(View):
    '''
    /rooms/:roomId/members/:memberId
    '''
    def put(self, request, roomId, memberId):
        pass
    def delete(self, request, roomId, memberId):
        pass
