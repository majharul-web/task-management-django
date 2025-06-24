from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskModelForm
from tasks.models import Task

# Create your views here.

def manager_dashboard(request):
    return render(request, 'dashboard/manager-dashboard.html')

def user_dashboard(request):
    return render(request, 'dashboard/user-dashboard.html')


def create_task(request):
    form = TaskModelForm() #For GET request, we pass employees to the form
    
    if(request.method == 'POST'): # If the request is POST, we need to process the form data
        form = TaskModelForm(request.POST)
        if form.is_valid():
            task = form.save()
            return render(request, 'task-form.html', {'form': form, 'message': 'Task created successfully!'})
            # return HttpResponse("Task created successfully!")
        
    context= {
        'form': form,
    }
    return render(request, 'task-form.html', context)

def view_tasks(request):
    tasks = Task.objects.all()  # Fetch all tasks from the database
    specific_tasks = Task.objects.get(id=1)  # Example of fetching a specific task by ID
    first_task = Task.objects.first()  # Fetch the first task in the database
    last_task = Task.objects.last()  # Fetch the last task in the database
    context = {
        'tasks': tasks,
        'specific_task': specific_tasks,
        'first_task': first_task,
        'last_task': last_task,
    }
    return render(request, 'view-tasks.html', context)