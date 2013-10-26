#!/usr/bin/env python
import os
import sys

from djangomango.settings.base import path

# insert the paths to apps
sys.path.insert(0, path('apps'))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangomango.settings")

    import djangomango.startup as startup
    startup.run()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
