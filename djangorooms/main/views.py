from math import frexp
from django.shortcuts import render
from .models import Room, Message


def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'main/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    messages = Message.objects.filter(room=pk)
    context = {'room': room, 'messages': messages}
    return render(request, 'main/room.html', context)


def createRoom(request):
    context = {}
    return render(request, 'main/room_form.html', context)