#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.environ.get('DEBUG', 'False').lower() == 'true':
        #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chajaa.settings.dev")
        os.environ["DJANGO_SETTINGS_MODULE"]= "chajaa.settings.dev"
    else:
        #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chajaa.settings.production")
        os.environ["DJANGO_SETTINGS_MODULE"]= "chajaa.settings.production"
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
