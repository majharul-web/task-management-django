from django.db.models.signals import post_save,pre_save,pre_delete,post_delete,m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task
from django.conf import settings

# Signal handlers for Task model
@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == "post_add":
        assigned_employees = [employee.email for employee in instance.assigned_to.all()]
        send_mail(
            subject=f"New Task Assigned: {instance.title}",
            message=f"You have been assigned a new task: {instance.title}.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=assigned_employees,
            fail_silently=False
        )

@receiver(post_delete, sender=Task)
def delete_task_details(sender, instance, **kwargs):
    if instance.details:
        instance.details.delete()
       
 
# @receiver(post_save, sender=Task)
# def notify_task_creation(sender, instance, created, **kwargs):
#     print("sender:", sender)
#     print("instance:", instance)
#     print("created:", created)
#     print("kwargs:", kwargs)
    
#     if created:
#         Task.objects.filter(pk=instance.pk).update(is_completed=True)

# @receiver(pre_save, sender=Task)
# def notify_task_update(sender, instance, **kwargs):
#     print("sender:", sender)
#     print("instance:", instance)
#     print("kwargs:", kwargs)

#     if instance.pk:  
#         instance.is_completed = True  

# @receiver(pre_delete, sender=Task)
# def notify_task_deletion(sender, instance, **kwargs):
#     print("sender:", sender)
#     print("instance:", instance)
#     print("kwargs:", kwargs)


# @receiver(post_delete, sender=Task)
# def notify_task_deleted(sender, instance, **kwargs):
#     print("sender:", sender)
#     print("instance:", instance)
#     print("kwargs:", kwargs)
 
