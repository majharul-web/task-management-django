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
from django.views.generic import ListView, DetailView,UpdateView,DeleteView,TemplateView
from django.urls import reverse_lazy


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
class ManagerDashboardView(TemplateView):
    template_name = 'dashboard/manager-dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_type = self.request.GET.get('type', 'all')

        base_query = Task.objects.select_related('details').prefetch_related('assigned_to')

        if task_type == 'completed':
            tasks = base_query.filter(status='COMPLETED')
        elif task_type == 'pending':
            tasks = base_query.filter(status='PENDING')
        elif task_type == 'in_progress':
            tasks = base_query.filter(status='IN_PROGRESS')
        else:
            tasks = base_query.all()

        counts = Task.objects.aggregate(
            total_task=Count('id'),
            completed_tasks=Count('id', filter=Q(status='COMPLETED')),
            pending_tasks=Count('id', filter=Q(status='PENDING')),
            in_progress_tasks=Count('id', filter=Q(status='IN_PROGRESS')),
        )

        context['tasks'] = tasks
        context['counts'] = counts
        return context
    
# @method_decorator(user_passes_test(is_employee, login_url='no-permission'), name='dispatch')
class EmployeeDashboardView(TemplateView):
    template_name = 'dashboard/employee-dashboard.html'



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



class UpdateTaskView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'tasks.change_task'
    login_url = 'sign-in'
    model = Task
    form_class = TaskModelForm
    template_name = 'task-form.html'
    context_object_name = 'task'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True  # Indicate that this is an update view
        context['task_form'] = self.get_form()
        
        if hasattr(self.object,'details') and self.object.details:
            context['task_detail_form'] = TaskDetailModelForm(instance=self.object.details)
        else:
            context['task_detail_form'] = TaskDetailModelForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES, instance=getattr(self.object, 'details', None))
        
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)  
            task_detail.task = task  
            task_detail.save()  
            messages.success(request, "Task updated successfully!")
            return redirect('update-task', self.object.id)
        
        return render(request, self.template_name, self.get_context_data(task_form=task_form, task_detail_form=task_detail_form))


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('tasks.delete_task', login_url='no-permission'), name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    # template_name = 'tasks/task_confirm_delete.html'  
    success_url = reverse_lazy('manager-dashboard')
    pk_url_kwarg = 'id' 

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.details:
            self.object.details.delete()
        self.object.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        messages.error(request, "Invalid request method.")
        return redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required("tasks.view_task", login_url='no-permission'), name='dispatch')
class TaskListView(ListView):
    model = Task
    template_name = "view-tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.select_related('details').prefetch_related('assigned_to').all()


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
        return redirect('admin-dashboard')
    return redirect('no-permission')