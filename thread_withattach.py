#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import time
import datetime
import smtplib
import ConfigParser
import argparse
import mimetypes
import random
import logging.handlers

from distutils import debug
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    BodyPath = configsectionmaps("PATHS")['body']
    AttachmentPath = configsectionmaps("PATHS")['attachment']
    From = configsectionmaps("FROM")
    To = configsectionmaps("TO")
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
    outer = MIMEMultipart()
    outer['From'] = rFrom
    outer['To'] = rTo
    outer['Subject'] = rSubject + " " +"%s" % datetime.datetime.\
        now().strftime("%d/%m/%Y %H:%M:%S:%f")

    if os.listdir(BodyPath):
        rBody = random.choice(os.listdir(BodyPath))
        ctype, encoding = mimetypes.guess_type(rBody)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)

        BodyOpen = open(BodyPath + "/" + rBody)
        msgBody = MIMEText(BodyOpen.read(), _subtype=subtype)
        BodyOpen.close()
    else:
        msgBody= ""
    if os.listdir(AttachmentPath):
        rAttachment = random.choice(os.listdir(AttachmentPath))
        ctype, encoding = mimetypes.guess_type(rAttachment)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            Attachment = open(AttachmentPath  + "/" + rAttachment)
            msgAttachment = MIMEText(Attachment.read(), _subtype=subtype)
            Attachment.close()
        elif maintype == 'image':
            Attachment = open(AttachmentPath  + "/" + rAttachment, 'rb')
            msgAttachment = MIMEImage(Attachment.read(), _subtype=subtype)
            Attachment.close()
        elif maintype == 'audio':
            Attachment = open(AttachmentPath  + "/" + rAttachment, 'rb')
            msgAttachment = MIMEAudio(Attachment.read(), _subtype=subtype)
            Attachment.close()
        else:
            Attachment = open(AttachmentPath  + "/" + rAttachment, 'rb')
            msgAttachment = MIMEBase(maintype, subtype)
            msgAttachment.set_payload(Attachment.read())
            Attachment.close()
    else:
        msgAttachment=""

    if msgBody:
        outer.attach(msgBody)

    if msgAttachment:
        encoders.encode_base64(msgAttachment)
        msgAttachment.add_header(
            'Content-Disposition', 'attachment', filename=rAttachment)
        outer.attach(msgAttachment)

    outer.preamble = "This is a multi-part message in MIME format."
    composed = outer.as_string()

    if outer.as_string():
        code = "220"
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
            output = e.args
            if output[0] != "timed out":
                code = str(output[0].values()[0][0])
                message = str(output[0].values()[0][1])
            else:
                code = "0"
                message = "Connection refused"
        myLogger.info(
            "Status : %s; ExecTime : %s (second); Detail : %s"
            % (code, (time.time() - start_time), message))
    else :
        print "Mail Data is Empty"
