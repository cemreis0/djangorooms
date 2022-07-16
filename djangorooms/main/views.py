from email import message
from itertools import count
from unicodedata import name
from django.db.models import Q
from django.shortcuts import redirect, render
from .models import Room, Message, Topic
from .forms import RoomForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    context = {'page': page}
    return render(request, 'main/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Bir hata oldu. Lütfen tekrar deneyin.')
    context = {'form': form}
    return render(request, 'main/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
        )
    room_count = rooms.count()
    topics = Topic.objects.all()
    roomMessages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, "topics":topics, "room_count": room_count, 'roomMessages': roomMessages}
    return render(request, 'main/home.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    roomMessages = Message.objects.filter(user=user)
    context = {'user':user, 'rooms':rooms, 'roomMessages':roomMessages}
    return render(request, 'main/profile.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    roomMessages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )  
        return redirect('room', pk=room.id)
    if request.user.is_authenticated:
        room.participants.add(request.user)
    context = {'room': room, 'roomMessages': roomMessages, "participants": participants}
    return render(request, 'main/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        topicName = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topicName)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')
    context = {'form': form, 'topics':topics}
    return render(request, 'main/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    roomURL = '/room/' + str(room.id)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('you are not allowed to do that')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect(roomURL)
    context = {'form': form, 'roomURL': roomURL, 'topics':topics}
    return render(request, 'main/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('you are not allowed to do that')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    return render(request, 'main/delete.html', context)


@login_required(login_url='login')
def deleteRoomMessage(request, pk):
    message = Message.objects.get(id=pk)
    messageRoomURL = '/room/' + str(message.room.id)
    if request.user != message.user:
        return HttpResponse('you are not allowed to do that')
    if request.method == 'POST':
        message.delete()
        return redirect(messageRoomURL)
    context = {'obj': message, 'messageRoomURL': messageRoomURL}
    return render(request, 'main/delete.html', context)