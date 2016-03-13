#!/usr/bin/env python

# BE CAREFUL! this will run in prod if you run it in prod. Don't be a doofus

import importlib, subprocess
import sys, os

sys.path.append("jamjar/jamjar/settings/")

settings_file = os.environ.get('JAMJAR_ENV')
settings = importlib.import_module(settings_file)

CONFIG = settings.LILO_CONFIG['database']

pres_file = './fingerprints_present_seed.sql'

cmd = "mysql --host='%s' --user='%s' --password='%s' < %s" % (CONFIG['host'], CONFIG['user'], CONFIG['passwd'], pres_file)


print "resetting presentation fingerprint data!!"
subprocess.call(cmd, shell=True)

