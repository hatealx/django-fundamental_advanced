from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import CreateUserForm, LoginForm, CreateTaskForm, UpdateUserForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from . models import Task
from django.contrib.auth.models import User


# Create your views here.


def home(request):    
    return render(request, 'index.html')




def register(request):
   form = CreateUserForm()
   if request.method == 'POST':
      form = CreateUserForm(request.POST)
      if form.is_valid:
         form.save()
         return redirect('my-login') 
   context = {'form': form}
   return render(request, 'register.html',context=context)


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





@login_required(login_url='my-login')
def dashboard(request):
   return render(request, 'profile/dashboard.html')



def logout(request):
   auth.logout(request)
   return redirect('')



@login_required(login_url='my-login')
def createTask(request):
   form = CreateTaskForm()

   if request.method == 'POST':
      form =  CreateTaskForm(request.POST)
      if form.is_valid():
         task = form.save(commit=False)
         task.user = request.user
         task.save()    # Create the Task object but don't save it yet
         
         return redirect('view_task')

   context =  {'form': form}
   return render(request, 'profile/create_task.html', context=context)


@login_required(login_url='my-login')
def viewTask(request):
   current_user = request.user.id
   task = Task.objects.all().filter(user=current_user)
   context  =  {"task":task}

   return render(request, 'profile/view_task.html', context=context)

  
@login_required(login_url='my-login')
def updateTask(request, pk):
   task = Task.objects.get(id=pk)
   form = CreateTaskForm(instance=task)
   if request.method == 'POST':
      form =  CreateTaskForm(request.POST, instance=task)
      if form.is_valid():
         form.save()
         return redirect('view_task')
   
   context =  {'form': form}

   return render(request, 'profile/update_task.html',context=context)

def deleteTask(request, pk):
   task = Task.objects.get(id=pk)
   if request.method == 'POST':
      task.delete()
      return redirect('view_task')
 
   return render(request, 'profile/delete_task.html')




@login_required(login_url='my-login')
def profileManagement(request):
   if request.method == 'POST':
      form =  UpdateUserForm(request.POST, instance=request.user)
      if form.is_valid():
         form.save()
         return redirect('dashboard')

   user_form  = UpdateUserForm(instance=request.user)
   

   context =  {'form': user_form}

   return render(request, 'profile/profile_management.html',context=context)


@login_required(login_url='my-login')
def deleteAccount(request):
   if request.method == 'POST':
      deleteUser = User.objects.get(username=request.user)
      deleteUser.delete()
      return redirect('')
   return render(request, 'profile/delete_account.html')


