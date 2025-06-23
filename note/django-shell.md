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
