#!/usr/bin/env python
import os, sys, codecs

if __name__ == "__main__":
    jamjar_env = os.environ.get('JAMJAR_ENV', None)

    if jamjar_env in ['prod', 'dev', 'test']:
        settings_module = "jamjar.settings.{}".format(jamjar_env)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    else:
        raise RuntimeError("No acceptable JAMJAR_ENV specified! Given: {}".format(jamjar_env))

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
