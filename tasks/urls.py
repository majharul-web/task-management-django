from django.urls import path
from tasks.views import HiGreetingView, manager_dashboard,employee_dashboard,create_task,update_task,delete_task,view_tasks,task_details,dashboard,GreetingView,HiGreetingView,CreateTaskView,ProjectView,DetailsView
urlpatterns = [
    path('manager-dashboard/',manager_dashboard,name='manager-dashboard'),
    path('employee-dashboard/',employee_dashboard,name='employee-dashboard'),
    path('create-task/', CreateTaskView.as_view(), name='create-task'),
    path('update-task/<int:id>/', update_task,name='update-task'),
    path('tasks/delete/<int:id>/', delete_task, name='delete-task'),  
    path('view-tasks/', view_tasks,name='view-tasks'),
    path('task-details/<int:id>/', DetailsView.as_view(),name='task-details'),
    #  path('task-details/<int:id>/', task_details,name='task-details'),
    
    path('dashboard/', dashboard, name='dashboard'),  # Redirect to dashboard view
    
    # class based views example
    path('greeting/', GreetingView.as_view(), name='greeting'),
    path('hi-greeting/', HiGreetingView.as_view(message="Hi, this is another custom class-based view!"), name='hi-greeting'),

    path('view-projects/',ProjectView.as_view(), name='view-projects'),  # Assuming view_tasks is used to view projects

]