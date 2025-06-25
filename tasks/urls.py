from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,create_task,view_tasks,related_tasks
urlpatterns = [
    path('manager-dashboard/',manager_dashboard),
    path('user-dashboard/',user_dashboard),
    path('create-task/', create_task),  
    path('view-tasks/', view_tasks),
    path('related-tasks/', related_tasks),
]