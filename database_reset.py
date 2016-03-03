#!/usr/bin/env python

# BE CAREFUL! this will run in prod if you run it in prod. Don't be a doofus

import importlib, subprocess
import sys, os

sys.path.append("jamjar/jamjar/settings/")

settings_file = os.environ.get('JAMJAR_ENV')
settings = importlib.import_module(settings_file)

CONFIG = settings.LILO_CONFIG['database']

drop_query = 'drop database if exists dejavu; drop database if exists dejavu_test;'
create_query = 'CREATE DATABASE IF NOT EXISTS dejavu; CREATE DATABASE IF NOT EXISTS dejavu_test'

cmd = "mysql --host='%s' --user='%s' --password='%s' -e '{}'" % (CONFIG['host'], CONFIG['user'], CONFIG['passwd'])


print "dropping dejavu dbs!!"
subprocess.call(cmd.format(drop_query), shell=True)

print "creating dejavu dbs!!"
subprocess.call(cmd.format(create_query), shell=True)


