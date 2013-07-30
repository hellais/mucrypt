import json
from base64 import b64encode, b64decode
from dh import DiffieHellman

class Identity(DiffieHellman):
    username = None
    server = None
    conference_address = None
    protocol = 'jabber'

    def __init__(self, path=None):
        super(Identity, self).__init__()
        if path:
            self.import_identity_file(path)
        else:
            self.generateKeys()

    def decrypt_private_key(self, password):
        raise NotImplemented

    def encrypt_private_key(self, password):
        raise NotImplemented

    def generate_public_key(self):
        return self.public_key
    
    def write_identity_file(self, path, password=None):
        content = { 'username': self.username,
                'server': self.server,
                'conference_address': self.conference_address,
                'protocol': self.protocol,
                'public_key': self.public_key,
                'private_key': self.private_key
        }
        if password:
            content['private_key'] = self.encrypt_private_key(password)
        with open(path, 'w') as f:
            f.write(json.dumps(content))

    def import_identity_file(self, path, password=None):

        with open(path) as f:
            identity = json.load(f)
        if password:
            self.decrypt_private_key(password)
        else:
            self.private_key = identity['private_key']

        self.username = identity['username']
        self.server = identity['server']
        self.conference_address = identity['conference_address']
        self.protocol = identity['protocol']
        self.public_key = identity['public_key']

class EphemeralIdentity(Identity):
    def generatePayload(self):
        payload = {'ephemeral_public_key': self.public_key,
        }
        return json.dumps(payload)


class State(object):
    pass


