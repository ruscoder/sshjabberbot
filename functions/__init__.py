# -*- coding: utf-8 -*-
import functions
import types
from functions import *
__author__ = 'ir4y'

def handle(command):
    for function_name in dir(functions):
        fun = globals()[function_name]
        if type(fun) == types.FunctionType and command == function_name:
            return fun(command)
    return u'Неизвестная команда'
