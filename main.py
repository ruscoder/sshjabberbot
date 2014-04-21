# -*- coding: utf-8 -*-
import sys
from twisted.internet import reactor
import sshjabberbot
import settings

__author__ = 'ir4y'

def main():
    reactor.connectTCP(settings.HOST, 5222, sshjabberbot.init_factory())
    return reactor.run()

if __name__ == "__main__":
    sys.exit(main())
