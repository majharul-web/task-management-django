from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,create_task,update_task,delete_task,view_tasks,related_tasks
urlpatterns = [
    path('manager-dashboard/',manager_dashboard,name='manager-dashboard'),
    path('user-dashboard/',user_dashboard,name='user-dashboard'),
    path('create-task/', create_task,name='create-task'),  
    path('update-task/<int:id>/', update_task,name='update-task'),
    path('delete-task/<int:id>/', delete_task,name='delete-task'),  
    path('view-tasks/', view_tasks,name='view-tasks'),
    path('related-tasks/', related_tasks,name='related-tasks'),
]