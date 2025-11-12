import os
import sys

def main():

    # Set the default Django settings module for this project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'email_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Raise a detailed error if Django is not installed or not accessible
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Pass command-line arguments to Django’s management utility
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
