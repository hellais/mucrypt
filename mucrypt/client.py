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

class MUCrypt(MUCClient):

    def __init__(self, roomJID, nick):
        MUCClient.__init__(self)
        self.roomJID = roomJID
        self.nick = nick


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

        MUCClient.connectionInitialized(self)

        d = self.join(self.roomJID, self.nick)
        @d.addCallback
        def cb(joinedRoom):
            print "Joined the room %s" % joinedRoom
        @d.addErrback
        def eb(joinedRoom):
            print "Joined failed to %s" % joinedRoom


    def receivedGroupChat(self, room, user, message):
        """
        Called when a groupchat message was received.

        Check if the message was addressed to my nick and if it said
        C{'hello'}. Respond by sending a message to the room addressed to
        the sender.
        """
        print "I GOT %s: %s" % (user.nick, message.body)
        if message.body.startswith("--BEGIN-MUCrypt--"):
            print "========================"
            self.groupChat(self.roomJID, "--GOT-IT--")

        if message.body.startswith(self.nick + u":"):
            nick, text = message.body.split(':', 1)
            text = text.strip().lower()
            if text == u'hello':
                body = u"%s: Hi!" % (user.nick)
                self.groupChat(self.roomJID, body)

# Set up the Twisted application

application = service.Application("MUC Client")

client = XMPPClient(THIS_JID, SECRET)
client.logTraffic = LOG_TRAFFIC
client.setServiceParent(application)

mucHandler = MUCrypt(ROOM_JID, NICK)
mucHandler.setHandlerParent(client)
