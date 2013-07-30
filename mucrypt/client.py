import re
import json

from twisted.internet import reactor
from twisted.application import service
from twisted.python import log
from twisted.words.protocols.jabber.jid import JID
from wokkel.client import XMPPClient
from wokkel.muc import MUCClient

# Configuration parameters

THIS_JID = JID('mucrypt@jabber.ccc.de')
ROOM_JID = JID('mucrypt@conference.jabber.ccc.de')
NICK = u'mucrypt@jabber.ccc.de'
SECRET = 'mucrypt'
LOG_TRAFFIC = True

class MUCryptMessage(object):
    pass

from parsley import makeGrammar
mucryptGrammar = """
mucryptBegin = '--BEGIN-MUCRYPT--'
mucryptEnd = '--BEGIN-MUCRYPT--'
mucryptComment = '\w'

mucryptMessage = mucryptBegin '\n' 
                 anything+ '\n'
                 (anything+):message \n'
                 mucryptEnd -> json.loads(message)
"""
mucryptGrammer.bindings({'json': json})
MucryptGrammer = makeGrammar(exampleGrammar, {})

class MUMessage(object):
    def __init__(self, content, user):
        self.content = content
        self.user = user

class UserInSessionAlready(Exception):
    pass


class MUSession(object):
    verified = None
    possibleStates = ['new', 'negotiating',
        'encrypted', 'authenticated']

    def __init__(self, member_count):
        self.members = {}
        self.member_count = member_count
        self.public_key_store = {}
        self.state = 'new'
        self.session_key = None

    def encypted(self):
        pass

    def addMember(self, nick, public_key):
        if nick in self.members:
            raise UserInSessionAlready
        else:
            self.members[nick] = public_key
            if self.member_count <= len(self.members.keys()):
                self.state = 'encrypted'
                self.encrypted()

    def verifyMembers(self):
        for nick, pub_key in self.members.items():
            if nick in self.public_key_store and \
                    self.public_key[nick] == self.pub_key:
                self.verified = True
                return self.verified
            else:
                self.verified = False
                return self.verified

class MUCrypt(MUCClient):

    def __init__(self, roomJID, nick):
        super(MUCClient, self).__init__()

        self.roomJID = roomJID
        self.nick = nick
        self.session = MUSession()

    def connectionInitialized(self):
        """
        Once authorized, join the room.

        If the join action causes a new room to be created, the room will be
        locked until configured. Here we will just accept the default
        configuration by submitting an empty form using L{configure}, which
        usually results in a public non-persistent room.

        Alternatively, you would use L{getConfiguration} to retrieve the
        configuration form, and then submit the filled in form with the
        required settings using L{configure}, possibly after presenting it to
        an end-user.
        """
        def joinedRoom(room):
            if room.locked:
                # Just accept the default configuration. 
                return self.configure(room.roomJID, {})

        super(MUCClient, self).connectionInitialized()

        d = self.join(self.roomJID, self.nick)
        @d.addCallback
        def cb(joinedRoom):
            print "Joined the room %s" % joinedRoom
        @d.addErrback
        def eb(joinedRoom):
            print "Joined failed to %s" % joinedRoom


    def processMessage(self, mu_message):
        # mu_message
        pass

    def receivedGroupChat(self, room, user, message):
        """
        Called when a groupchat message was received.

        Check if the message was addressed to my nick and if it said
        C{'hello'}. Respond by sending a message to the room addressed to
        the sender.
        """
        self.sendMUCryptMessage({'foobar': "Hello world"})

        if message.body.startswith("--BEGIN-MUCRYPT--"):
            message_content = MucryptGrammer(message.body).mucryptMessage()
            mu_message = MUMessage(message_content, user)
            self.processMessage(mu_message)

        if message.body.startswith(self.nick + u":"):
            nick, text = message.body.split(':', 1)
            text = text.strip().lower()
            if text == u'hello':
                body = u"%s: Hi!" % (user.nick)
                self.groupChat(self.roomJID, body)

    def sendMUCryptMessage(self, message):
        payload =  "--BEGIN-MUCRYPT--\n"
        payload += "This message is encrypted with Mucrypt. To learn more about Mucrypt visit: https://github.com/hellais/greenhouse.\n"
        payload += "\n\r\n\r"
        payload += "%s" % json.dumps(data)
        payload += "--END-MUCRYPT--"

# Set up the Twisted application

application = service.Application("MUC Client")

client = XMPPClient(THIS_JID, SECRET)
client.logTraffic = LOG_TRAFFIC
client.setServiceParent(application)

mucHandler = MUCrypt(ROOM_JID, NICK)
mucHandler.setHandlerParent(client)
