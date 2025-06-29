## Django Shell Commands

### Start Django Shell

```bash
python manage.py shell
```

### Import Models

```python
from app_name.models import ModelName
# Example: from tasks.models import Task
```

### Create and Save an Instance

```python
instance = ModelName(field1='value1', field2='value2')
instance.save()
# example: task = Task(title="Task 1",description="Task 1 description",due_date="2024-12-12")
# task.save()

```

### Create instance with `create()`

```python
instance = ModelName.objects.create(field1='value1', field2='value2')
# example: task = Task.objects.create(title="Task 1",description="Task 1 description",due_date="2024-12-12")
```

### Get an Instance

```python
instance = ModelName.objects.get(pk=1)
# example: task = Task.objects.get(id=1)
```

### Get & Create TaskDetails for a Task

```python
from tasks.models import Task, TaskDetail
task = Task.objects.get(id=1)
task_details = TaskDetails.objects.create(task=task, assigned_to="John Doe", priority="H")
```

### Create Project

```python
from tasks.models import Project
project = Project.objects.create(name="Project 1", start_date="2024-01-01")
allprojects = Project.objects.all()
first_project_id = Project.objects.first().id
```

### Create Employee and Assign to Task

```python
from tasks.models import Employee,Task
# Create an employee
employee1 = Employee.objects.create(name="John Doe", email="john.doe@example.com")
employee2 = Employee.objects.create(name="Jane Smith", email="jane.smith@example.com")

# create task
task1 = Task.objects.create(title="Task 1", description="Task 1 description", due_date="2024-12-12")

task1.assigned_to.add(employee1)  # Assign employee to task
task1.assigned_to.add(employee2)  # Assign another employee to the same task

task1.assigned_to.all()  # Get all employees assigned to the task

# import all from tasks.models
from tasks.models import *
task_details = TaskDetail.objects.get(id=1) # Get a specific task detail
task_details.task # Get the task associated with the task detail
task_details.task.title # Get the title of the task associated with the task detail
task1.taskdetail # Get the task detail associated with the task

employee1.task_set.all()  # Get all tasks assigned to employee1
employee2.tasks.all().first()  # Get all tasks assigned to employee2

```

### Add test data using Faker

```python
from populate_db import populate_db
populate_db()  # This will populate the database with test data
```

### Practice task

<!-- `1. Show the tasks which are assigned to a specific employee -->

```python
from tasks.models import *
employee = Employee.objects.get(pk=1)
tasks = employee.tasks.all()
for task in tasks:
    print(task.title, task.description, task.due_date)
```

<!--2. Show all employees working on a specific project -->

```python
from tasks.models import *
project = Project.objects.get(pk=1)
tasks = Task.objects.filter(project=project)
employees = Employee.objects.filter(tasks__in=tasks).distinct()
for employee in employees:
    print(employee.name, employee.email)
```

<!-- Get all tasks that are due today -->

```python
from tasks.models import *
from datetime import date
tasks = Task.objects.filter(due_date=date.today())
for task in tasks:
    print(task.title, task.description)
```

<!-- 4. Show all tasks with a priority higher than 'low' -->

```python
from tasks.models import *
tasks = Task.objects.select_related('details').filter(details__priority__in=['H', 'M'])
for task in tasks:
    print(task.title, task.priority)
```

<!-- Get the number of tasks completed by a specific employee -->

```python
from tasks.models import *
employee = Employee.objects.get(pk=4)
tasks = employee.tasks.filter(status='COMPLETED').count()

print(f"Number of completed tasks for {employee.name}: {tasks}")
```

<!-- Get the most recently assigned task -->

```python
from tasks.models import *
task = Task.objects.order_by('-created_at').first()
print(f"Most recently assigned task: {task.title}")
```

<!-- Show all projects that have no tasks assigned -->

```python
from tasks.models import *
projects = Project.objects.filter(task__isnull=True)

from django.db.models import Count
from tasks.models import Project

projects_without_tasks = Project.objects.annotate(
    task_count=Count('task')
).filter(task_count=0)

for project in projects_without_tasks:
    print(project.name)
```

<!-- Show tasks that have been overdue for more than a week -->

```python
from datetime import date, timedelta
from tasks.models import Task

one_week_ago = date.today() - timedelta(days=7)

overdue_tasks = Task.objects.filter(
    due_date__lt=one_week_ago,
    is_completed=False
)

# Example: Print overdue task titles and due dates
for task in overdue_tasks:
    print(f"{task.title} — Due on {task.due_date}")

```

<!-- Get the total count of tasks assigned to each employee -->

```python
from tasks.models import *
from django.db.models import Count

employees = Employee.objects.annotate(task_count=Count('tasks'))
for employee in employees:
    print(employee.name, employee.task_count)
```

<!-- Get tasks that are either 'completed' or 'in-progress' -->

```python
from tasks.models import *
tasks = Task.objects.filter(status__in=['COMPLETED', 'IN_PROGRESS'])
for task in tasks:
    print(task.title, task.status)
```
