from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskModelForm

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