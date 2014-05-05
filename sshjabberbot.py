# -*- coding: utf-8 -*-
from twisted.words.protocols.jabber import jid
from twisted.words.xish import domish
from functions import handle
from advanced_jabberclient.jabberclient import jabberClientFactory

import settings


__author__ = 'badim'


def init_factory():
    def authd(xmlstream):
        presence = domish.Element(('jabber:client', 'presence'))
        xmlstream.send(presence)

        def gotMessage(message):
            answer = None
            for e in message.elements():
                if e.name == "body":
                    command = e.__str__()
                    if command == "ping":
                        xmlstream.receivePing()
                    else:
                        answer = handle(command)

            if answer:
                xmlstream.sendMessage(message["from"], answer)

        xmlstream.addObserver('/message',  gotMessage)

    factory = jabberClientFactory(jid=jid.JID(settings.USERNAME),
                                  secret=settings.PASSWORD,
                                  ping_timeout=settings.PING_TIMEOUT,
                                  ping_fail_time=settings.PING_FAIL_TIME,
                                  host=settings.HOST)

    factory.addBootstrap('//event/stream/authd', authd)
    return factory

