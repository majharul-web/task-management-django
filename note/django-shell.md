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
