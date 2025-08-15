from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
)
from .models import Task
from .serializers import RegisterSerializer, TaskSerializer
from .tokens import get_tokens_for_user

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  
    
class CustomLoginView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({
                'refresh': tokens['refresh'],
                'access': tokens['access'],
                'username': user.username, 
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class TaskListAPIView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskRetrieveAPIView(RetrieveAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskCreateAPIView(CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TaskUpdateAPIView(UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDestroyAPIView(DestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
def register_template(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'register.html')


def login_template(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('task-list-template')
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@permission_classes([IsAuthenticated])
def task_list_view(request):
    # tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html')


@permission_classes([IsAuthenticated])
def task_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(user=request.user, title=title, description=description)
        return redirect('task-list-template')
    return render(request, 'tasks/task_form.html')


@permission_classes([IsAuthenticated])
def task_update_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.save()
        return redirect('task-list-template')
    return render(request, 'tasks/task_form.html', {'task': task})


@permission_classes([IsAuthenticated])
def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task-list-template')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})