from django.shortcuts import render

# Create your views here.
def gameStart(request):
    return render(request, 'snake.html')
