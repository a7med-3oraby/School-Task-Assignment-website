from django.shortcuts import render, redirect
from .models import Task
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
def index(request):
    return render(request, 'index.html')




@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        is_admin = data.get('admin', False)
        
        if not username or not email or not password:
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        if is_admin:
            user.is_staff = True
            user.is_superuser = True
        user.save()
        
        return JsonResponse({'success': 'User created successfully'}, status=201)
    
    elif request.method == 'GET':
        return render(request, 'signup.html')
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'success': 'Login successful', 'type': 'Admin' if user.is_staff else 'Teacher'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    elif request.method == 'GET':
        return render(request, 'login.html')
    return JsonResponse({'error': 'Invalid request method'}, status=405)
def teacher_home(request):
    return render(request, 'teacher_home.html', {'username': request.user.username})

def view_teacher_tasks(request):
    if request.user.is_authenticated :
        tasks = Task.objects.filter(teacher=request.user, completed=False)
        return render(request, 'viewTeachertasks.html', {'tasks': tasks})
    else:
        return redirect('login')

def teacher_completed_tasks(request):
    if request.user.is_authenticated :
        tasks = Task.objects.filter(teacher=request.user, completed=True)
        return render(request, 'teacher_completed_tasks.html', {'tasks': tasks})
    else:
        return redirect('login')
    
def admin_home(request):
     return render(request, 'admin_home.html', {'username': request.user.username})
def admin_add_task(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task_title = data.get('task_title')
        task_priority = data.get('task_priority')
        task_description = data.get('task_description')
        task_teacher_name = data.get('teacher_name')

        if not task_title or not task_priority or not task_description or not task_teacher_name:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        try:
            teacher = User.objects.get(username=task_teacher_name) 
            # Check if the teacher is staff or superuser
            if teacher.is_staff or teacher.is_superuser:
                return JsonResponse({'error': 'Teacher cannot be admin'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Teacher does not exist'}, status=400)

        if Task.objects.filter(title=task_title).exists():
            return JsonResponse({'error': 'Task title already in use'}, status=400)

        Task.objects.create(
            title=task_title,
            priority=task_priority,
            description=task_description,
            admin=request.user,
            teacher=teacher
        )
        return JsonResponse({'success': 'Task added successfully'})

    return render(request, 'admin_add_task.html')

def tasklist(request):
    tasks = Task.objects.filter(admin=request.user)
    return render(request, 'tasklist.html', {'tasks': tasks})
def task_details(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_details.html', {'task': task})

def delete_task(request, task_id):
    if request.method == 'DELETE':
        try:
            task = Task.objects.get(id=task_id, admin=request.user)
            task.delete()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def edit_task(request, task_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('teacher')
        try:
            user = User.objects.get(username=username)
            
            if user.is_staff or user.is_superuser:
                return JsonResponse({'error': 'The teacher must not be admin'}, status=400)

            task = get_object_or_404(Task, id=task_id)
            task.title = data.get('title')
            task.priority = data.get('priority')
            task.description = data.get('description')
            task.teacher = user
            task.save()
            return JsonResponse({'success': 'Task updated successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Teacher does not exist'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def mark_task_complete(request, task_id):
    if request.method == 'POST' and request.user.is_authenticated :
        task = get_object_or_404(Task, id=task_id, teacher=request.user)
        task.completed = True
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def check_teacher_exists(request, teacher_name):
    if User.objects.filter(username=teacher_name).exists():
        return JsonResponse({'exists': True})
    else:
        return JsonResponse({'exists': False})




