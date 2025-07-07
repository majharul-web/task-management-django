from django.urls import path
from tasks.views import manager_dashboard,employee_dashboard,create_task,update_task,delete_task,view_tasks,task_details
urlpatterns = [
    path('manager-dashboard/',manager_dashboard,name='manager-dashboard'),
    path('employee-dashboard/',employee_dashboard,name='employee-dashboard'),
    path('create-task/', create_task,name='create-task'),  
    path('update-task/<int:id>/', update_task,name='update-task'),
    path('delete-task/<int:id>/', delete_task,name='delete-task'),  
    path('view-tasks/', view_tasks,name='view-tasks'),
    path('task-details/<int:id>/', task_details,name='task-details'),

]