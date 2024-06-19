from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from .models import Task, Post
from .forms import TaskForm, PostForm, CommentForm


def is_admin(user):
    """Function to check if the user is superuser(admin)."""
    return user.is_superuser


@login_required
def dashboard(request):
    """Function to return the dashboard for request."""
    return render(request, 'the_app/dashboard.html')


def home(request):
    """Function to return the homepage for request."""
    return render(request, 'the_app/home.html')


def register(request):
    """Function to register users, checks if the username is already taken.
    also logs the user in after a successful registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration successful!')
                return redirect('home')
            else:
                messages.error(request, 'Unable to log in after registration.')
        else:
            messages.error(request,
                           'Registration failed. Please\
                            correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'the_app/register.html', {'form': form})


def login_view(request):
    """Function to log the user in."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'the_app/login.html')


@login_required
def task_list(request):
    """Function to view the task list also checks if the task is
    expired"""
    tasks = Task.objects.filter(user=request.user)
    for task in tasks:
        if task.is_expired():
            messages.warning(request, f'Task "{task.title}" is expired!')
    return render(request, 'the_app/task_list.html', {'tasks': tasks})


@login_required
def task_add(request):
    """Function to add a task and save it to the database"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'the_app/task_add.html', {'form': form})


@login_required
def task_edit(request, task_id):
    """Function to edit the selected task."""
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'the_app/task_edit.html',
                  {'form': form, 'task': task})


@login_required
def task_delete(request, task_id):
    """Function to delete the selected task."""
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'the_app/task_delete.html', {'task': task})


@login_required
def logout_view(request):
    """Logs the user out and takes them to the homepage."""
    logout(request)
    return redirect(reverse_lazy('home'))


@login_required
def admin_dashboard(request):
    """Function to view the admin dashboard only for admin."""
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    users = User.objects.all()
    return render(request, 'the_app/admin_dashboard.html', {'users': users})


@login_required
def admin_user_tasks(request, user_id):
    """Function to see every task for any users. Only for admin"""
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    user = User.objects.get(id=user_id)
    tasks = Task.objects.filter(user=user)
    return render(request, 'the_app/admin_user_tasks.html',
                  {'tasks': tasks, 'user': user})


@login_required
def admin_delete_user(request, user_id):
    """Only the admin can delete users."""
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('admin_dashboard')
    return render(request, 'the_app/admin_delete_user.html', {'user': user})


@login_required
def admin_delete_task(request, task_id):
    """Admin can delete user's tasks"""
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('admin_user_tasks', user_id=task.user.id)
    return render(request, 'the_app/admin_delete_task.html', {'task': task})


@login_required
def admin_edit_task(request, task_id):
    """Admin can edit the user's task"""
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('admin_user_tasks', user_id=task.user.id)
        else:
            messages.error(request,
                           'Failed to update task.\
                            Please correct the errors below.')
    else:
        form = TaskForm(instance=task)
    return render(request, 'the_app/admin_edit_task.html',
                  {'form': form, 'task': task})


@login_required
def admin_add_task(request, user_id):
    """Admin can add tasks for the user."""
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('admin_user_tasks', user_id=user.id)
        else:
            messages.error(request,
                           'Failed to add task.\
                            Please correct the errors below.')
    else:
        form = TaskForm()
    return render(request, 'the_app/admin_add_task.html',
                  {'form': form, 'user': user})


def post_list(request):
    """List view for the bulletin board."""
    posts = Post.objects.all()
    return render(request, 'the_app/post_list.html', {'posts': posts})


def post_detail(request, post_id):
    """Function to make commenting possible at the bulletin board."""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'the_app/post_detail.html',
                  {'post': post, 'comments': comments, 'form': form})


@login_required
@user_passes_test(is_admin)
def post_add(request):
    """Posting a new bulletin topic. Only for admin."""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'the_app/post_form.html', {'form': form})
