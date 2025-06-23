from django.db import models

# Create your models here.
class Task(models.Model):
    project= models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        default='1'  
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   

class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    )
    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=2, choices=PRIORITY_OPTIONS, default=LOW)
    

class Project(models.Model):
    name= models.CharField(max_length=200)
    start_date = models.DateField()