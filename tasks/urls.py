from django.urls import path
from tasks.views import HiGreetingView, ManagerDashboardView,TaskListView,dashboard,GreetingView,HiGreetingView,CreateTaskView,ProjectView,DetailsView,UpdateTaskView,TaskDeleteView,EmployeeDashboardView
urlpatterns = [
    path('manager-dashboard/',ManagerDashboardView.as_view(),name='manager-dashboard'),
    path('employee-dashboard/',EmployeeDashboardView.as_view(),name='employee-dashboard'),
    path('create-task/', CreateTaskView.as_view(), name='create-task'),
    # path('update-task/<int:id>/', update_task,name='update-task'),
    path('update-task/<int:pk>/', UpdateTaskView.as_view(), name='update-task'),  # Using UpdateTaskView for class-based view
    path('tasks/delete/<int:id>/', TaskDeleteView.as_view(), name='delete-task'),
    path('view-tasks/', TaskListView.as_view(),name='view-tasks'),
    path('task-details/<int:id>/', DetailsView.as_view(),name='task-details'),
    #  path('task-details/<int:id>/', task_details,name='task-details'),
    
    path('dashboard/', dashboard, name='dashboard'),  # Redirect to dashboard view
    
    # class based views example
    path('greeting/', GreetingView.as_view(), name='greeting'),
    path('hi-greeting/', HiGreetingView.as_view(message="Hi, this is another custom class-based view!"), name='hi-greeting'),

    path('view-projects/',ProjectView.as_view(), name='view-projects'),  # Assuming view_tasks is used to view projects

]