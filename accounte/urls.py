from django.urls import path

from .views import (
    TaskListCreateAPIView,
    TaskListView,
    TaskDetailView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    UserLoginView,
    UserLogoutView,
    UserRegisterView,
    UserListView,
    profile_view,
    SuperUserSeaAllTasks
    
)

urlpatterns = [
   
    path('', TaskListView.as_view(), name='home'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('profile/', profile_view, name='profile'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('tasks/list/', SuperUserSeaAllTasks.as_view(), name='tasks-list'),
    # path('api/tasks/', TaskListCreateAPIView.as_view(), name='api-tasks'),
]
