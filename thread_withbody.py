#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import time
import smtplib
import ConfigParser
import argparse
import random
import logging.handlers

from distutils import debug

COMMASPACE = ', '

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

# Usage settings from Argparse method
hostname=socket.gethostname()
parser = argparse.ArgumentParser(
    description='Use to determine the number of workers.')
parser.add_argument('-t', action="store",
                    dest="threadNum", type=int)
parser.add_argument('-p', action="store",
                    dest="processNum", type=int)
args = parser.parse_args()
threadNum = args.threadNum
processNum = args.processNum

if not threadNum:
    exit()
if not processNum:
    exit()

processCount = int(1)
processNumint = int(processNum)

# For loop from processNum
processNumint=processNumint+1
for i in range(1, processNumint):
    # Read config and get variables from config.ini
    Config = ConfigParser.ConfigParser()
    Config.read("config.ini")
    From = configsectionmaps("FROM")
    To = configsectionmaps("TO")
    filePath = configsectionmaps("PATHS")['emlfile']
    logFile = configsectionmaps("PATHS")['log']
    Subjects = configsectionmaps("SUBJECTS")
    Host = configsectionmaps("SERVER")['host']
    Port = configsectionmaps("SERVER")['port']
    timeOut = int(configsectionmaps("SERVER")['timeout'])

    # Set the logger mechanism
    myLogger = logging.getLogger(
        "Thread : %s; Process : %s" % (threadNum, i))
    myLogger.setLevel(logging.INFO)
    HANDLER = logging.handlers.RotatingFileHandler(
        logFile, maxBytes=100 * 1024 * 1024)
    FORMATTER = logging.Formatter(
        '%(asctime)s; %(name)s (%(process)s); %(message)s')
    HANDLER.setFormatter(FORMATTER)
    myLogger.addHandler(HANDLER)

    # Selecting random variable
    rFrom = random.choice(From.values())
    rTo = random.choice(To.values())
    rSubject = random.choice(Subjects.values())

    # Generating Mail Elements and Parts
    if filePath :
        filename = random.choice(os.listdir(filePath))
        filename="emlfiles/" + filename
        f = open(filename, 'r')
        composed = f.read()
        f.close()
        code = "250"
        message = "OK"
        start_time = time.time()
        try:
            if timeOut is not None:
                s = smtplib.SMTP(Host, Port, hostname, timeOut)
            else:
                s = smtplib.SMTP(Host, Port, hostname)
            s.sendmail(rFrom, rTo, composed)
            s.quit()
        except Exception as e:
            output = str(e)
            code = "0"
            message = "Sending Problem : " + output
        myLogger.info(
            "Status : %s; ExecTime : %s (second); Detail : %s"
            % (code, (time.time() - start_time), message))
    else :
        print "Mail Data is Empty"
