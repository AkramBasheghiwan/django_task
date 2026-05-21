from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework import generics
from .serializers import TaskSerializer
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ProfileForm, UserLoginForm, UserRegisterForm,TaskForm
from .models import Profile, Task





# def task_list(request):
#     tasks = Task.objects.all()
#     return render(request, 'accounte/task_list.html', {'tasks': tasks})
#
# def task_detail(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     return render(request, 'accounte/task_detail.html', {'task': task})
#
# def task_create(request):
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.owner = request.user
#             task.save()
#             return redirect('task-detail', pk=task.pk)
#     else:
#         form = TaskForm()
#     return render(request, 'accounte/task_form.html', {'form': form})
#
# def task_update(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('task-detail', pk=task.pk)
#     else:
#         form = TaskForm(instance=task)
#     return render(request, 'accounte/task_form.html', {'form': form})
#
# def task_delete(request, pk):
#     task = get_object_or_404(Task, pk=pk)
#     if request.method == 'POST':
#         task.delete()
#         return redirect('task-list')
#     return render(request, 'accounte/task_confirm_delete.html', {'task': task})
#
# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(request, data=request.POST)
#         if form.is_valid():
#             login(request, form.get_user())
#             return redirect('task-list')
#     else:
#         form = UserLoginForm()
#     return render(request, 'accounte/login.html', {'form': form})
#
# def user_register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('task-list')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'accounte/register.html', {'form': form})
#
@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounte/profile.html', {'form': form})





class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'accounte/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
       



class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'accounte/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)





class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'completed']
    template_name = 'accounte/task_form.html'
    

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task-detail',kwargs ={'pk':self.object.pk})
    




        
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'completed']
    template_name = 'accounte/task_form.html'
    
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy('task-detail', kwargs={'pk': self.object.pk})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'accounte/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')
   
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)



class UserLoginView(LoginView):
    template_name = 'accounte/login.html'
    authentication_form = UserLoginForm
    # redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'accounte/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Ensure a Profile object exists for the new user.
        Profile.objects.get_or_create(user=self.object)
        return response


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم تحديث ملفك الشخصي بنجاح.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'accounte/profile.html', {'form': form})

class SuperUserSeaAllTasks(LoginRequiredMixin,UserPassesTestMixin,ListView):
    model = Task
    template_name ='accounte/tasks_list.html'
    context_object_name ='taskss'
    
    def test_func(self):
        return self.request.user.is_superuser
        
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.success('لاتوجد لديك صلاحيه لرويه هذه الصفحه')
            return redirect('tasks-list')
         
        return super().handle_no_permission()
                     
     



class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounte/user_list.html'
    context_object_name = 'users'
    paginate_by = 25

    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        # If user is authenticated but not allowed, redirect with message.
        if self.request.user.is_authenticated:
            messages.error(self.request, 'غير مصرح لك برؤية هذه الصفحة.')
            return redirect('task-list')
        # Otherwise, fallback to default (redirect to login)
        return super().handle_no_permission()


class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer