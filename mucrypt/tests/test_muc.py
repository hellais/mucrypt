import sys
import os

# Hack to set the proper sys.path. Overcomes the export PYTHONPATH pain.
sys.path[:] = map(os.path.abspath, sys.path)
sys.path.insert(0, os.path.abspath(os.getcwd()))

from unittest import TestCase, main

from mucrypt.client import MUSession, MUCrypt

class MockMUCryptClient(MUCrypt):
    def __init__(self):
        self.messages = []
        roomJID = 0
        nick = 'mock'
        super(MockMUCryptClient, self).__init__(roomJID, nick)

    def processMessage(self, mu_message):
        msg = mu_message.content
        nick = mu_message.user.nick
        self.received_message(self, nick, msg)

    def groupChat(self, jid, body):
        self.messages.append((self.nick, body))

    def send(self, msg):
        self.groupChat(0, msg)

    def receivedGroupChat(self, room, user, message):
        self.received_message(self, user.nick, message.body)
        super(MockMUCryptClient, self).receivedGroupChat(room, user, message)

    def received_message(self, nick, msg):
        self.messages.append((nick, msg))

class MockGroupChat(object):
    protocol = MockMUCrypt

    def __init__(self, clients):
        self.clients = clients
        self.protocol.received_message = self.received_message

    def send_message(self, msg):
        self.protocol.send(msg)
        for client in self.clients:
            client.received(msg)

    def received_message(self, msg):
        for client in self.clients:
            client.received(msg)

class DummyClient(object):
    def received(self, msg):
        print "----"
        print "I Received this message"
        print "----"
        print msg
        print "----"

class TestMUCrypt(TestCase):
    def setUp(self):
        client1 = DummyClient()
        client2 = DummyClient()
        client3 = DummyClient()
        self.clients = [client1, client2, client3]
        self.groupChat = MockGroupChat(self.clients)

    def test_group_chat(self):
        self.groupChat.send_message("Hello world!")
        print "y00y0y0y0"
        print self.groupChat.protocol.messages

    def test_recv_public_key(self):
        pass

if __name__ == '__main__':
    main()
