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

### Querying Models

```python
# create a new instance
instance = ModelName(field1='value1', field2='value2')
instance.save()
# example: task = Task(title="Task 1",description="Task 1 description",due_date="2024-12-12")
# task.save()

```
