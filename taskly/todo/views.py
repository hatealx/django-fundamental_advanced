from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm, CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):    
    return render(request, 'index.html')

def login(request):
   form =  LoginForm
   if request.method == 'POST':
      form =  LoginForm(request, data=request.POST)
      if form.is_valid():
        username = request.POST.get('username')
        password =  request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')

   context =  {'form': form}
   return render(request, 'login.html', context=context)
def logout(request):
   auth.logout(request)
   return redirect('')

def createTask(request):
   form =  TaskForm()
   if request.method == 'POST':
      form =  TaskForm(request.POST)
      if form.is_valid():
         form.save()
         return redirect('view-task')
      
         
   
   context =  {'form': form}
   return render(request, 'task_form.html', context = context)

def ViewTasks(request):
   tasks = Task.objects.all()
   context = {'tasks' : tasks}

   return render(request, 'view_tasks.html', context=context)


def updateTasks(request, pk):
   task = Task.objects.get(id=pk)
   form =  TaskForm(instance=task)
   if request.method == 'POST':
      form =  TaskForm(request.POST, instance=task)
      if form.is_valid():
         form.save()
         return redirect('view-task')
   
   context =  {'form': form}


   return render(request, 'update.html',context=context )


def deleteTasks(request, pk):
   task = Task.objects.get(id=pk)
   if request.method == 'POST':
      task.delete()
      return redirect('view-task')
   
   context =  {'object': task}
   return render(request, 'delete.html', context=context)


def register(request):
   form = CreateUserForm()
   if request.method == 'POST':
      form = CreateUserForm(request.POST)
      if form.is_valid:
         form.save()
         return HttpResponse('the user was registered')
   context = {'form': form}
   return render(request, 'register.html',context=context)
@login_required(login_url='my-login')
def dashboard(request):
   return render(request, 'dashboard.html')