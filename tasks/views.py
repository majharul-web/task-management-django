from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskModelForm,TaskDetailModelForm
from tasks.models import Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Count
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from users.views import is_admin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import ListView, DetailView


create_task_decorators = [login_required, permission_required('tasks.add_task', login_url='no-permission')]
# Class based views example
class GreetingView(View):
    message="Hello, this is a class-based view!"
    def get(self, request):
        return HttpResponse(self.message)

class HiGreetingView(View):
    message="Hi, this is another class-based view!"
    def get(self, request):
        return HttpResponse(self.message)



# helper function
def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

# @user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    type= request.GET.get('type', 'all')  # Get the type from query parameters, default to 'all'
    print(type)
    base_query= Task.objects.select_related('details').prefetch_related('assigned_to')
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    else:
        tasks = base_query.all()
        
    counts=Task.objects.aggregate(
        total_task=Count('id'),
        completed_tasks=Count('id', filter=Q(status='COMPLETED')),
        pending_tasks=Count('id', filter=Q(status='PENDING')),
        in_progress_tasks=Count('id', filter=Q(status='IN_PROGRESS'))
    )
    
    context = {
        'tasks': tasks,
        'counts': counts,
    }
    return render(request, 'dashboard/manager-dashboard.html',context=context)

@user_passes_test(is_employee, login_url='no-permission')
def employee_dashboard(request):
    return render(request, 'dashboard/employee-dashboard.html')


@login_required
@permission_required('tasks.add_task', login_url='no-permission')
def create_task(request):
    task_form = TaskModelForm() 
    task_detail_form = TaskDetailModelForm()  

    if(request.method == 'POST'): # If the request is POST, we need to process the form data
        task_form = TaskModelForm(request.POST)  
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        print("v",request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)  
            task_detail.task = task  
            task_detail.save()  
            messages.success(request, "Task created successfully!")
            return redirect('create-task')
            # return HttpResponse("Task created successfully!")
        
    context= {
        'task_form': task_form,
        'task_detail_form': task_detail_form,
        'is_update': False,
    }
    return render(request, 'task-form.html', context)


# Create task class based view example
# @method_decorator(create_task_decorators, name='dispatch')
class CreateTaskView(LoginRequiredMixin,PermissionRequiredMixin,ContextMixin, View):
    permission_required = 'tasks.add_task'
    login_url = 'sign-in'  
    template_name = 'task-form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        context['task_detail_form'] = kwargs.get('task_detail_form', TaskDetailModelForm())
        context['is_update'] = False
        return context

    def get(self, request):
        context = self.get_context_data()
        return render(request, 'task-form.html', context)

    def post(self, request):
        task_form = TaskModelForm(request.POST)  
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)  
            task_detail.task = task  
            task_detail.save()  
            messages.success(request, "Task created successfully!")
            # return redirect('create-task')
            context = self.get_context_data(task_form=task_form, task_detail_form=task_detail_form)
            return render(request, 'task-form.html', context)

class ProjectView(LoginRequiredMixin, PermissionRequiredMixin, ListView, View):
    permission_required = 'tasks.view_project'
    login_url = 'sign-in'

    model = Project
    context_object_name = 'projects'
    template_name = 'view-projects.html'

    def get_queryset(self):
        return Project.objects.annotate(task_count=Count('task')).order_by('-task_count')

@login_required
@permission_required('tasks.change_task', login_url='no-permission')
def update_task(request,id):
    task = Task.objects.get(pk=id)  # Fetch the task to be updated
    task_form = TaskModelForm(instance=task)
    if(task.details):
        task_detail_form = TaskDetailModelForm(instance=task.details)
    

    if(request.method == 'POST'): # If the request is POST, we need to process the form data
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST,request.FILES, instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)  
            task_detail.task = task  
            task_detail.save()  
            messages.success(request, "Task updated successfully!")
            return redirect('update-task', id=task.id)
            # return HttpResponse("Task created successfully!")
        
    context= {
        'task_form': task_form,
        'task_detail_form': task_detail_form,
        'is_update': True,
    }
    return render(request, 'task-form.html', context)

@login_required
@permission_required('tasks.delete_task', login_url='no-permission')
def delete_task(request, id):
    task = get_object_or_404(Task, pk=id)

    if request.method == 'POST':
        # Optional: delete related detail if it exists
        try:
            task.details.delete()
        except TaskDetail.DoesNotExist:
            pass  # No detail to delete

        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('manager-dashboard')

    messages.error(request, "Invalid request method.")
    return redirect('manager-dashboard')

@login_required
@permission_required('tasks.view_task', login_url='no-permission')
def view_tasks(request):
    tasks = Task.objects.all()  # Fetch all tasks from the database
    count_all_tasks = Task.objects.aggregate(count=Count('id'))  # Count all tasks
    specific_tasks = Task.objects.get(pk=5)  # Example of fetching a specific task by ID
    first_task = Task.objects.first()  # Fetch the first task in the database
    last_task = Task.objects.last()  # Fetch the last task in the database
    tasks_by_status = Task.objects.filter(status='PENDING')  # Example of filtering tasks by status
    tasks_by_due_date = Task.objects.filter(due_date=date.today())  # Example of filtering tasks by due date
    tasks_by_priority = TaskDetail.objects.exclude(priority='H')  # Example of filtering tasks by priority

    # example of contains
    filter_task_using_and_contains = Task.objects.filter(title__icontains='c',status='PENDING')  #use and using comma separated values
    filter_task_using_or = Task.objects.filter(Q(status="IN_PROGRESS") | Q(status='PENDING'))  #use or using Q objects 
    
    check_is_exists = Task.objects.filter(title__icontains='urgent').exists()  # Check if any task contains 'urgent' in the title

    task_count_in_project=Project.objects.annotate(task_count=Count('task')).order_by('-task_count')  # Count tasks in each project

    context = {
        'tasks': tasks,
        'count_all_tasks': count_all_tasks['count'],
        'specific_task': specific_tasks,
        'first_task': first_task,
        'last_task': last_task,
        'tasks_by_status': tasks_by_status,
        'tasks_by_due_date': tasks_by_due_date,
        'tasks_by_priority': tasks_by_priority,
        'filter_task_using_and_contains': filter_task_using_and_contains,
        'filter_task_using_or': filter_task_using_or,
        'check_is_exists': check_is_exists,
        'task_count_in_project': task_count_in_project,
    }
    return render(request, 'view-tasks.html', context)

@login_required
@permission_required('tasks.view_task', login_url='no-permission')
def task_details(request, id):
    task = Task.objects.get(pk=id)  
    status_choices = Task.STATUS_CHOICES  
    
    if request.method == 'POST':
        new_status = request.POST.get('task_status')
        if new_status:
            task.status = new_status
            task.save()
            messages.success(request, "Task status updated successfully!")
            return redirect('task-details', id=task.id)
        else:
            messages.error(request, "Invalid status selection.")
            return redirect('task-details', id=task.id)
    context = {
        'task': task,
        'status_choices': status_choices,
    }
    return render(request, 'task-details.html', context)

class DetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = 'tasks.view_task'
    login_url = 'sign-in'
    pk_url_kwarg = 'id'  # Use 'id' as the URL parameter for the task ID
    model = Task
    template_name = 'task-details.html'
    context_object_name = 'task'
    
    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Task.STATUS_CHOICES
        return context
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        new_status = request.POST.get('task_status')
        if new_status:
            task.status = new_status
            task.save()
            messages.success(request, "Task status updated successfully!")
            return redirect('task-details', id=task.id)
        else:
            messages.error(request, "Invalid status selection.")
            return redirect('task-details', id=task.id)
    

@login_required
def dashboard(request):
    pass
    if is_manager(request.user):
        return redirect('manager-dashboard')
    elif is_employee(request.user):
        return redirect('employee-dashboard')
    elif is_admin(request.user):
        return redirect('manager-dashboard')
    return redirect('no-permission')