<<<<<<< HEAD
#!/usr/bin/env python3.10
=======
#!/usr/bin/env python
>>>>>>> 96823c6827b23b7a7529a75e690ef3a64981c7b8
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FaceDetection.settings')
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
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 96823c6827b23b7a7529a75e690ef3a64981c7b8
