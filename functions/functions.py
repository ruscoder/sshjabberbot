# -*- coding: utf-8 -*-
import datetime
from subprocess import  PIPE,Popen
import settings

__author__ = 'ir4y'

def time(command):
    return datetime.datetime.now().__str__()

def get_rsa_pub(command):
    return open(settings.RSA_PATH).read()

def connect_back(command):
    #ssh -R 2000:localhost:5555 localhost -p 5555
    Popen(["/usr/bin/ssh", "-R","2222:localhost:22","{0}@{1}".format(settings.SSH_HOST_USER,settings.SSH_HOST),"-p",settings.SSH_HOST_PORT])
    return "tunnel_created"

