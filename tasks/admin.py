from django.contrib import admin
from tasks.models import Task, Project, TaskDetail, Employee

# Register your models here.
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(TaskDetail)
admin.site.register(Employee)
