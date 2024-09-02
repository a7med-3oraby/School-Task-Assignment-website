from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/',views.login,name='login'),
    path('teacher_home/',views.teacher_home,name='teacher_home'),
    path('viewTeachertasks/', views.view_teacher_tasks, name='viewTeachertasks'),
    path('teacher_completed_tasks/', views.teacher_completed_tasks, name='teacher_completed_tasks'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('admin_add_task/',views.admin_add_task,name='admin_add_task'),
    path('tasklist/',views.tasklist,name='tasklist'),
    path('task_details/<int:task_id>/', views.task_details, name='task_details'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('mark_task_complete/<int:task_id>/', views.mark_task_complete, name='mark_task_complete'),
    path('check_teacher_exists/<str:teacher_name>/', views.check_teacher_exists, name='check_teacher_exists'),




]

