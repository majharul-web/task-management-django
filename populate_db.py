import os
import django
import random
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

from tasks.models import Project, Task, TaskDetail
from django.contrib.auth import get_user_model

User = get_user_model()

def populate_db():
    fake = Faker()

    # Create Projects
    projects = [
        Project.objects.create(
            name=fake.bs().capitalize(),
            description=fake.text(),
            start_date=fake.date_this_year()
        )
        for _ in range(5)
    ]
    print(f"✅ Created {len(projects)} projects.")

    # Create Users
    employees = [
        User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            is_active=True,
            password='Majharul@1#%'  # ✅ Set fixed password
        )
        for _ in range(10)
    ]
    print(f"✅ Created {len(employees)} users.")


    # Create Tasks
    tasks = []
    for _ in range(20):
        task = Task.objects.create(
            project=random.choice(projects),
            title=fake.sentence(nb_words=4),
            description=fake.paragraph(nb_sentences=3),
            due_date=fake.date_this_year(),
            status=random.choice(['PENDING', 'IN_PROGRESS', 'COMPLETED']),
        )
        # Assign random 1-3 users
        assigned_users = random.sample(employees, random.randint(1, 3))
        task.assigned_to.set(assigned_users)
        tasks.append(task)
    print(f"✅ Created {len(tasks)} tasks and assigned users.")

    # Create TaskDetails
    for task in tasks:
        TaskDetail.objects.create(
            task=task,
            # asset: Skipped for now since you're not uploading real images
            priority=random.choice(['H', 'M', 'L']),
            notes=fake.paragraph()
        )
    print(f"✅ Created TaskDetails for all tasks.")

    print("🎉 Database populated successfully!")

if __name__ == "__main__":
    populate_db()
