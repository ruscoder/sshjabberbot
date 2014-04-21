# -*- coding: utf-8 -*-
from time import time
from twisted.words.protocols.jabber import xmlstream, client, jid
from twisted.words.xish import domish
from functions import handle
import settings
__author__ = 'ir4y'


class PingXmlStream(xmlstream.XmlStream):
    def __init__(self, authenticator):
        xmlstream.XmlStream.__init__(self, authenticator)
        self.ping_received_time = time()

    def checkPong(self):
        self.sendPing()
        if time() - self.ping_received_time >= settings.PING_FAIL_TIME:
            self.transport.loseConnection()
        else:            
            self._callLater(settings.PING_TIMEOUT, self.checkPong)

    def sendPing(self):
        msg = domish.Element(("jabber:client", "message"))
        msg["to"] = "echo.{0}".format(settings.HOST)
        msg.addElement("body", content="ping")
        self.send(msg)

    def receivePing(self):
        self.ping_received_time = time()

    def connectionMade(self):
        xmlstream.XmlStream.connectionMade(self)
        self._callLater(settings.PING_TIMEOUT, self.checkPong)


class ReconnectClientFactory(xmlstream.XmlStreamFactory):
    protocol = PingXmlStream

    def __init__(self, authenticator):
        xmlstream.XmlStreamFactory.__init__(self, authenticator)
        self.maxDelay = 10


def jabberClientFactory(jid, secret):
    a = client.BasicAuthenticator(jid, secret)
    return ReconnectClientFactory(a)


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

            msg = domish.Element(("jabber:client", "message"))
            msg["to"] = message["from"]
            msg.addElement("body", content=answer)
            xmlstream.send(msg)

        xmlstream.addObserver('/message',  gotMessage)


    factory = jabberClientFactory(jid.JID(settings.USERNAME), settings.PASSWORD)
    factory.addBootstrap('//event/stream/authd', authd)
    return factory

