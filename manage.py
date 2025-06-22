#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# create a virtual environment: python -m venv venv
# linux venv activate: source venv/bin/activate
# linux deactivate: deactivate
# windows venv activate: venv\Scripts\activate
# create requirements.txt: pip freeze > requirements.txt
# install dependencies: pip install -r requirements.txt
# see dependencies: pip list
# make migrations: python manage.py makemigrations
# migrate database: python manage.py migrate
# run shell: python manage.py shell
# run-server: python manage.py runserver
