from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm
from tasks.models import Employee,Task

# Create your views here.

def manager_dashboard(request):
    return render(request, 'dashboard/manager-dashboard.html')

def user_dashboard(request):
    return render(request, 'dashboard/user-dashboard.html')


def create_task(request):
    employees = Employee.objects.all()
    form = TaskForm(employees=employees) #For GET request, we pass employees to the form
    
    if(request.method == 'POST'): # If the request is POST, we need to process the form data
        form = TaskForm(request.POST, employees=employees)
        if form.is_valid():
            data= form.cleaned_data
            title = data['title']
            description = data['description']
            due_date = data['due_date']
            assigned_to = data['assigned_to']

            task = Task.objects.create(
                title=title,
                description=description,
                due_date=due_date
            )
           
            # for employee_id in assigned_to:
            for employee_id in assigned_to:
                employee = Employee.objects.get(id=employee_id)
                task.assigned_to.add(employee)
            return HttpResponse("Task created successfully!")
        
    context= {
        'form': form,
    }
    return render(request, 'task-form.html', context)