from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponse
import json

# Create your views here.
def gameStart(request):
    return render(request, 'snake.html')

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

