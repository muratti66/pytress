#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import ConfigParser
import subprocess

from distutils import debug

# Config Define from Example
def configsectionmaps(section):
    dictOne = {}
    options = Config.options(section)
    for option in options:
        try:
            dictOne[option] = Config.get(section, option)
            if dictOne[option] == -1:
                debug.debugprint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dictOne[option] = None
    return dictOne

Config = ConfigParser.ConfigParser()
Config.read("config.ini")
host = configsectionmaps("SERVER")['host']
thread = int(configsectionmaps("SENDING")['thread'])
amount = int(configsectionmaps("SENDING")['amount'])

intThread= thread + 1

for x in range(0, intThread):
    subprocess.Popen([sys.executable,"./thread.py", "-t %s" % x, "-p %s" % amount], close_fds=True)
total=amount * thread
print "%s emails sent to host : %s" % (total,host)
