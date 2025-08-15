from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
TokenObtainPairView,
TokenRefreshView
)
from .views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
     # API endpoints for authentication
    path('cregister/', RegisterView.as_view(), name='api-register'),
    path('custom-login/', CustomLoginView.as_view(), name='api-login'),

    # API endpoints for Task CRUD
    path('api/tasks/', TaskListAPIView.as_view(), name='api-task-list'),
    path('api/tasks/<int:pk>/', TaskRetrieveAPIView.as_view(), name='api-task-detail'),
    path('api/tasks/create/', TaskCreateAPIView.as_view(), name='api-task-create'),
    path('api/tasks/<int:pk>/update/', TaskUpdateAPIView.as_view(), name='api-task-update'),
    path('api/tasks/<int:pk>/delete/', TaskDestroyAPIView.as_view(), name='api-task-delete'),

    # Template URLs for task management
    path('c-register/', register_template, name='register'),
    path('login/', login_template, name='login'),
    path('tasks/', task_list_view, name='task-list-template'),
    path('tasks/create/', task_create_view, name='task-create-template'),
    path('tasks/<int:pk>/edit/', task_update_view, name='task-update-template'),
    path('tasks/<int:pk>/delete/', task_delete_view, name='task-delete-template'),
    path('logout/', views.logout_view, name='logout'),

]

