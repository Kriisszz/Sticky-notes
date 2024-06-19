from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/add/', views.task_add, name='task_add'),
    path('tasks/edit/<int:task_id>/', views.task_edit, name='task_edit'),
    path('tasks/delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/<int:user_id>/tasks/',
         views.admin_user_tasks, name='admin_user_tasks'),
    path('admin-dashboard/users/<int:user_id>/delete/',
         views.admin_delete_user, name='admin_delete_user'),
    path('admin-dashboard/tasks/<int:task_id>/edit/',
         views.admin_edit_task, name='admin_edit_task'),
    path('admin-dashboard/tasks/<int:task_id>/delete/',
         views.admin_delete_task, name='admin_delete_task'),
    path('admin-dashboard/users/<int:user_id>/tasks/add/',
         views.admin_add_task, name='admin_add_task'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/add/', views.post_add, name='post_add'),

]
