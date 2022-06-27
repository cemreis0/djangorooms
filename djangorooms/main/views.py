from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')

def room(request):
    return render(request, 'main/room.html')