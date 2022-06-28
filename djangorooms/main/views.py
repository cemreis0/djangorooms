from math import frexp
from django.shortcuts import redirect, render
from .models import Room, Message
from .forms import RoomForm


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
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'main/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'main/room_form.html', context)


def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'main/delete.html', {'obj': room})