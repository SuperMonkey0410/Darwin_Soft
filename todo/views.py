from django.contrib import auth
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, permissions, status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse
from .models import Task, TaskPermission, User
from .serializers import TaskSerializer, TaskPermissionSerializer, UserSerializer
from .forms import UserLoginForm, RegistrationForm, ProfileForm
from django.contrib.auth.decorators import login_required



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        creator_id = self.request.data.get('id')  # Получаем ID пользователя из запроса
        if creator_id:
            creator = User.objects.get(id=creator_id)  # Получаем объект пользователя по ID
            serializer.save(creator=creator)
        else:
            serializer.save()  # Сохраняем задачу без указания создателя, если не выбран пользователь

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.AllowAny()]
        return super().get_permissions()


class TaskPermissionViewSet(viewsets.ModelViewSet):
    queryset = TaskPermission.objects.all()
    serializer_class = TaskPermissionSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    # def get_permissions(self):
    #     if self.action in ['create', 'update', 'destroy']:
    #         return [permissions.IsAuthenticated()]
    #     return super().get_permissions()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = make_password(serializer.validated_data['password'])  # хэшируем пароль user
        serializer.save(password=password)


"""Регистрация и авторизация  ( на основе форм ) """

def register(request, ):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance  # делаем так, чтобы юзер после регистрации, не прописывал логин заново
            auth.login(request, user)
            return HttpResponseRedirect(reverse('#'))

    else:
        form = RegistrationForm()
    context = {'form': form}

    return render(request, '#', context=context)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)

                return HttpResponseRedirect('#')
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, '#', context=context)

@login_required
def logout(request, ):
    auth.logout(request)
    return redirect(reverse('#'))
