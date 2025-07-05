from django.db import models
from django.db.models.signals import post_save,pre_save,pre_delete,post_delete
from django.dispatch import receiver

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # task_set
    
    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    # std_id=models.CharField(max_length=200, primary_key=True, unique=True)
    project= models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        default='1'  
    )
    assigned_to=models.ManyToManyField(Employee,related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
   

class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    )
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name='details',
    )
    # assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=2, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Details for {self.task.title}"


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    
    def __str__(self):
        return self.name

from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Task  # Update with your actual import

@receiver(post_save, sender=Task)
def notify_task_creation(sender, instance, created, **kwargs):
    print("sender:", sender)
    print("instance:", instance)
    print("created:", created)
    print("kwargs:", kwargs)
    
    if created:
        # Avoid recursion by using update()
        Task.objects.filter(pk=instance.pk).update(is_completed=True)

@receiver(pre_save, sender=Task)
def notify_task_update(sender, instance, **kwargs):
    print("sender:", sender)
    print("instance:", instance)
    print("kwargs:", kwargs)

    if instance.pk:  # update scenario
        instance.is_completed = True  # Just set, it will be saved

@receiver(pre_delete, sender=Task)
def notify_task_deletion(sender, instance, **kwargs):
    print("sender:", sender)
    print("instance:", instance)
    print("kwargs:", kwargs)
    # Don't save — the object is about to be deleted

@receiver(post_delete, sender=Task)
def notify_task_deleted(sender, instance, **kwargs):
    print("sender:", sender)
    print("instance:", instance)
    print("kwargs:", kwargs)
    # Don't save — the object is already deleted
