# -*- coding: utf-8 -*-
from twisted.words.protocols.jabber import client, jid
from twisted.words.xish import domish
from functions import handle
import settings

__author__ = 'ir4y'


def init_factory():
    def authd(xmlstream):
        presence = domish.Element(('jabber:client','presence'))
        xmlstream.send(presence)
        def gotMessage(message):
            answer = None
            for e in message.elements():
                if e.name == "body":
                    answer = handle(e.__str__())

            msg = domish.Element(("jabber:client", "message"))
            msg["to"] = message["from"]
            msg.addElement("body", content = answer)
            xmlstream.send(msg)
        xmlstream.addObserver('/message',  gotMessage)

    factory = client.basicClientFactory(jid.JID(settings.USERNAME), settings.PASSWORD)
    factory.addBootstrap('//event/stream/authd',authd)
    return factory

